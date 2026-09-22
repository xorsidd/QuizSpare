from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from quiz.models import Category, Question, Option, QuizAttempt, AttemptAnswer


class QuizSphereStudentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create student user
        self.student = User.objects.create_user(
            username='test_student',
            email='student@test.com',
            password='password123'
        )
        
        # Create category
        self.category = Category.objects.create(
            name='Django Test Category',
            slug='django-test-category',
            description='Testing Django features',
            time_limit_mins=5,
            pass_percentage=60
        )
        
        # Create Question 1 (Slide 2 Sample Question)
        self.q1 = Question.objects.create(
            category=self.category,
            text='Which language is Django written in?',
            marks=2,
            explanation='Django is written in Python.'
        )
        self.q1_opt1 = Option.objects.create(question=self.q1, text='Java', is_correct=False)
        self.q1_opt2 = Option.objects.create(question=self.q1, text='Python', is_correct=True)
        self.q1_opt3 = Option.objects.create(question=self.q1, text='C++', is_correct=False)
        
        # Create Question 2
        self.q2 = Question.objects.create(
            category=self.category,
            text='Which architecture does Django use?',
            marks=1,
            explanation='Django uses MVT pattern.'
        )
        self.q2_opt1 = Option.objects.create(question=self.q2, text='MVC', is_correct=False)
        self.q2_opt2 = Option.objects.create(question=self.q2, text='MVT', is_correct=True)

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'QuizSphere')
        self.assertContains(response, 'Demo Student 1')
        self.assertContains(response, 'Django Test Category')

    def test_category_list_page(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Test Category')

    def test_presentation_showcase_page(self):
        response = self.client.get(reverse('presentation_showcase'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django MVT Pattern')
        self.assertContains(response, 'Slide 1')

    def test_quiz_detail_page(self):
        response = self.client.get(reverse('category_detail', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Test Category')

    def test_quiz_take_requires_login(self):
        url = reverse('quiz_take', kwargs={'slug': self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_quiz_submission_and_auto_grading(self):
        self.client.login(username='test_student', password='password123')
        
        post_data = {
            f'question_{self.q1.id}': str(self.q1_opt2.id),
            f'question_{self.q2.id}': str(self.q2_opt1.id),
            'time_taken_seconds': '45',
        }
        submit_url = reverse('quiz_submit', kwargs={'slug': self.category.slug})
        response = self.client.post(submit_url, data=post_data)
        
        self.assertEqual(response.status_code, 302)
        attempt = QuizAttempt.objects.filter(user=self.student, category=self.category).first()
        self.assertIsNotNone(attempt)
        self.assertEqual(attempt.score, 2)
        self.assertEqual(attempt.total_marks, 3)
        self.assertAlmostEqual(attempt.percentage, 66.7, places=1)
        self.assertTrue(attempt.passed)

        # Check result view
        result_response = self.client.get(reverse('quiz_result', kwargs={'attempt_id': attempt.id}))
        self.assertEqual(result_response.status_code, 200)
        self.assertContains(result_response, 'Examination Passed')
        self.assertContains(result_response, 'Python')

    def test_leaderboard(self):
        QuizAttempt.objects.create(
            user=self.student,
            category=self.category,
            score=3,
            total_marks=3,
            percentage=100.0,
            time_taken_seconds=30,
            passed=True
        )
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_student')

    def test_dashboard(self):
        self.client.login(username='test_student', password='password123')
        QuizAttempt.objects.create(
            user=self.student,
            category=self.category,
            score=3,
            total_marks=3,
            percentage=100.0,
            time_taken_seconds=30,
            passed=True
        )
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_student')
        self.assertContains(response, 'Attempt History')
