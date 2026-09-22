from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max, Avg, Count, Sum, Q
from django.http import HttpResponseForbidden

from .models import Category, Question, Option, QuizAttempt, AttemptAnswer
from .forms import RegistrationForm


def home(request):
    """
    Landing page: features, available quizzes, statistics, and presentation info.
    """
    categories = Category.objects.all().prefetch_related('questions')
    total_quizzes_taken = QuizAttempt.objects.count()
    total_questions = Question.objects.count()
    total_users = QuizAttempt.objects.values('user').distinct().count()
    recent_attempts = QuizAttempt.objects.select_related('user', 'category').order_by('-date_taken')[:5]

    context = {
        'categories': categories,
        'total_quizzes_taken': total_quizzes_taken,
        'total_questions': total_questions,
        'total_users': total_users,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'quiz/home.html', context)


def category_list(request):
    """
    Lists all available quiz categories with search capability.
    """
    search_query = request.GET.get('q', '').strip()
    categories = Category.objects.all().prefetch_related('questions')
    
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    context = {
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'quiz/category_list.html', context)


def quiz_detail(request, slug):
    """
    Pre-quiz briefing page: rules, time limit, question count, pass score, previous attempts.
    """
    category = get_object_or_404(Category, slug=slug)
    questions = category.questions.all()
    
    user_best_attempt = None
    user_attempt_count = 0
    if request.user.is_authenticated:
        attempts = QuizAttempt.objects.filter(user=request.user, category=category)
        user_attempt_count = attempts.count()
        user_best_attempt = attempts.order_by('-score', '-percentage').first()

    context = {
        'category': category,
        'questions_count': questions.count(),
        'total_marks': sum(q.marks for q in questions),
        'user_best_attempt': user_best_attempt,
        'user_attempt_count': user_attempt_count,
    }
    return render(request, 'quiz/quiz_detail.html', context)


@login_required
def quiz_take(request, slug):
    """
    The live quiz taking engine with countdown timer, radio options, and question navigator.
    """
    category = get_object_or_404(Category, slug=slug)
    questions = list(category.questions.prefetch_related('options').all())

    if not questions:
        messages.warning(request, f"The category '{category.name}' currently has no questions.")
        return redirect('category_detail', slug=slug)

    context = {
        'category': category,
        'questions': questions,
        'time_limit_seconds': category.time_limit_mins * 60,
    }
    return render(request, 'quiz/quiz_take.html', context)


@login_required
def quiz_submit(request, slug):
    """
    Submits answers, compares against correct options, stores QuizAttempt & AttemptAnswer,
    calculates score, percentage and pass/fail status.
    """
    if request.method != 'POST':
        return redirect('quiz_take', slug=slug)

    category = get_object_or_404(Category, slug=slug)
    questions = category.questions.prefetch_related('options').all()
    
    total_marks = 0
    earned_marks = 0
    time_taken_seconds = int(request.POST.get('time_taken_seconds', 0))

    # Create QuizAttempt record
    attempt = QuizAttempt.objects.create(
        user=request.user,
        category=category,
        score=0,
        total_marks=0,
        percentage=0.0,
        time_taken_seconds=time_taken_seconds,
        passed=False
    )

    attempt_answers = []
    for q in questions:
        total_marks += q.marks
        selected_option_id = request.POST.get(f'question_{q.id}')
        selected_option = None
        is_correct = False
        marks_for_q = 0

        if selected_option_id:
            try:
                selected_option = q.options.get(id=int(selected_option_id))
                if selected_option.is_correct:
                    is_correct = True
                    marks_for_q = q.marks
                    earned_marks += marks_for_q
            except (Option.DoesNotExist, ValueError):
                selected_option = None

        attempt_answers.append(
            AttemptAnswer(
                attempt=attempt,
                question=q,
                selected_option=selected_option,
                is_correct=is_correct,
                marks_obtained=marks_for_q
            )
        )

    AttemptAnswer.objects.bulk_create(attempt_answers)

    percentage = round((earned_marks / total_marks * 100), 1) if total_marks > 0 else 0.0
    passed = percentage >= category.pass_percentage

    attempt.score = earned_marks
    attempt.total_marks = total_marks
    attempt.percentage = percentage
    attempt.passed = passed
    attempt.save()

    messages.success(request, f"Quiz submitted successfully! You scored {earned_marks}/{total_marks} ({percentage}%).")
    return redirect('quiz_result', attempt_id=attempt.id)


@login_required
def quiz_result(request, attempt_id):
    """
    Displays instant feedback, detailed answer audit, correctness, explanation, and leaderboard rank.
    """
    attempt = get_object_or_404(QuizAttempt.objects.select_related('category', 'user'), id=attempt_id)
    
    # Restrict viewing to the student who attempted it
    if attempt.user != request.user:
        return HttpResponseForbidden("You do not have permission to view this quiz result.")

    answers = attempt.answers.select_related('question', 'selected_option').prefetch_related('question__options').all()

    # Calculate user rank in this category
    better_attempts = QuizAttempt.objects.filter(
        category=attempt.category,
        percentage__gt=attempt.percentage
    ).count()
    rank = better_attempts + 1

    context = {
        'attempt': attempt,
        'answers': answers,
        'rank': rank,
    }
    return render(request, 'quiz/quiz_result.html', context)


def leaderboard(request):
    """
    Live Leaderboard ranking top performers by category and overall.
    """
    category_id = request.GET.get('category')
    categories = Category.objects.all()

    attempts = QuizAttempt.objects.select_related('user', 'category')
    if category_id:
        attempts = attempts.filter(category_id=category_id)

    top_attempts = attempts.order_by('-percentage', '-score', 'time_taken_seconds')[:25]

    selected_category = None
    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            pass

    context = {
        'categories': categories,
        'top_attempts': top_attempts,
        'selected_category': selected_category,
    }
    return render(request, 'quiz/leaderboard.html', context)


@login_required
def user_dashboard(request):
    """
    Personal student dashboard displaying attempt history, performance stats, and badges.
    """
    attempts = QuizAttempt.objects.filter(user=request.user).select_related('category').order_by('-date_taken')
    total_attempts = attempts.count()
    passed_attempts = attempts.filter(passed=True).count()
    avg_score = attempts.aggregate(Avg('percentage'))['percentage__avg'] or 0.0
    highest_score = attempts.aggregate(Max('percentage'))['percentage__max'] or 0.0

    context = {
        'attempts': attempts,
        'total_attempts': total_attempts,
        'passed_attempts': passed_attempts,
        'pass_rate': round((passed_attempts / total_attempts * 100), 1) if total_attempts > 0 else 0,
        'avg_score': round(avg_score, 1),
        'highest_score': round(highest_score, 1),
    }
    return render(request, 'quiz/dashboard.html', context)


def register_view(request):
    """
    Student registration view.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f"Welcome to QuizSphere, {user.username}! Your student account is ready.")
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'quiz/register.html', {'form': form})


def login_view(request):
    """
    Student login view.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'quiz/login.html', {'form': form})


def logout_view(request):
    """
    Logs the user out and clears session.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


def presentation_showcase(request):
    """
    Project Presentation & Architecture Showcase page:
    All 12 slides, Django MVT visualizer, ERD schema, and team member roll numbers.
    """
    return render(request, 'quiz/presentation_showcase.html')
