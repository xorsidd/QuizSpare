from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """
    Quiz Category / Subject Model
    Stores categories like Python, Django, Web Development, Database Systems, etc.
    """
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    description = models.TextField(help_text="Overview of the quiz subject")
    icon = models.CharField(max_length=60, default="bi-lightbulb", help_text="Bootstrap icon class")
    time_limit_mins = models.PositiveIntegerField(default=10, help_text="Duration in minutes")
    pass_percentage = models.PositiveIntegerField(default=60, help_text="Passing score percentage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def total_questions(self):
        return self.questions.count()

    def total_marks(self):
        return sum(q.marks for q in self.questions.all())

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Question Model belonging to a Category.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(help_text="The question prompt")
    marks = models.PositiveIntegerField(default=1, help_text="Marks for correct answer")
    explanation = models.TextField(blank=True, help_text="Explanation shown after grading")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"[{self.category.name}] {self.text[:60]}"

    def correct_option(self):
        return self.options.filter(is_correct=True).first()


class Option(models.Model):
    """
    Options / Choices for a multiple-choice question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"


class QuizAttempt(models.Model):
    """
    Records an end-to-end user quiz attempt, timestamp, score, and completion status.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)
    total_marks = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    time_taken_seconds = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    date_taken = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_taken']

    def __str__(self):
        return f"{self.user.username} - {self.category.name} ({self.score}/{self.total_marks})"


class AttemptAnswer(models.Model):
    """
    Stores individual question responses submitted in a quiz attempt for full audit & review.
    """
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Attempt #{self.attempt_id} - Q: {self.question_id}"
