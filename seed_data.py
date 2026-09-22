import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizsphere_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from quiz.models import Category, Question, Option, QuizAttempt, AttemptAnswer
from django.utils import timezone
from datetime import timedelta

print("Starting QuizSphere database seeding...")

# 1. Create Users
admin_user, _ = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@quizsphere.local', 'is_staff': True, 'is_superuser': True}
)
admin_user.set_password('admin123')
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.save()

student_user, _ = User.objects.get_or_create(
    username='student',
    defaults={'email': 'student@quizsphere.local'}
)
student_user.set_password('student123')
student_user.save()

demo1_user, _ = User.objects.get_or_create(
    username='demo_student1',
    defaults={'email': 'student1@quizsphere.local'}
)
demo1_user.set_password('pass123')
demo1_user.save()

demo2_user, _ = User.objects.get_or_create(
    username='demo_student2',
    defaults={'email': 'student2@quizsphere.local'}
)
demo2_user.set_password('pass123')
demo2_user.save()

demo3_user, _ = User.objects.get_or_create(
    username='demo_student3',
    defaults={'email': 'student3@quizsphere.local'}
)
demo3_user.set_password('pass123')
demo3_user.save()

print(f"Users created: {User.objects.count()}")

# 2. Create Categories
categories_data = [
    {
        'name': 'Django Web Framework',
        'slug': 'django-web-framework',
        'description': 'Test your knowledge of Django MVT pattern, ORM queries, URL dispatcher, CSRF security, and session handling.',
        'icon': 'bi-braces-asterisk',
        'time_limit_mins': 5,
        'pass_percentage': 60,
    },
    {
        'name': 'Python Core & Concepts',
        'slug': 'python-core-concepts',
        'description': 'Master Python data structures, decorators, list comprehensions, exceptions, and object-oriented programming.',
        'icon': 'bi-filetype-py',
        'time_limit_mins': 5,
        'pass_percentage': 60,
    },
    {
        'name': 'Web Technologies & Bootstrap 5',
        'slug': 'web-technologies-bootstrap-5',
        'description': 'Assess your understanding of HTML5 semantics, CSS3 grid & flexbox, and Bootstrap 5 responsive utility classes.',
        'icon': 'bi-layout-text-window-reverse',
        'time_limit_mins': 5,
        'pass_percentage': 60,
    },
    {
        'name': 'Database Systems & SQL',
        'slug': 'database-systems-sql',
        'description': 'Evaluate relational database fundamentals, Primary Keys, Foreign Keys, SQLite vs PostgreSQL, and SQL injection prevention.',
        'icon': 'bi-database-check',
        'time_limit_mins': 5,
        'pass_percentage': 60,
    }
]

created_categories = {}
for cat_data in categories_data:
    cat, _ = Category.objects.update_or_create(
        slug=cat_data['slug'],
        defaults=cat_data
    )
    created_categories[cat.slug] = cat

print(f"Categories created: {len(created_categories)}")

# 3. Create Questions & Options
questions_data = [
    # Category 1: Django Framework
    {
        'category': 'django-web-framework',
        'text': 'Which language is Django written in? (Slide 2 Sample Question)',
        'marks': 1,
        'explanation': 'Django is an open-source web framework written completely in Python.',
        'options': [
            ('Java', False),
            ('Python', True),
            ('C++', False),
            ('PHP', False),
        ]
    },
    {
        'category': 'django-web-framework',
        'text': 'Which architectural design pattern does Django strictly follow? (Slide 5)',
        'marks': 1,
        'explanation': 'Django implements the Model-View-Template (MVT) pattern, where the View handles business logic and Templates handle UI.',
        'options': [
            ('Model-View-Controller (MVC)', False),
            ('Model-View-Template (MVT)', True),
            ('Single Page Application (SPA)', False),
            ('Microkernel Architecture', False),
        ]
    },
    {
        'category': 'django-web-framework',
        'text': 'Which component in Django is responsible for mapping an incoming URL path to a view function? (Slide 5)',
        'marks': 1,
        'explanation': 'The URL Dispatcher in urls.py matches HTTP request patterns and delegates execution to views.py.',
        'options': [
            ('models.py', False),
            ('URL Dispatcher (urls.py)', True),
            ('wsgi.py', False),
            ('admin.py', False),
        ]
    },
    {
        'category': 'django-web-framework',
        'text': 'How does Django safeguard web forms against Cross-Site Request Forgery? (Slide 10)',
        'marks': 1,
        'explanation': 'Django uses the {% csrf_token %} template tag and CsrfViewMiddleware to generate and validate unique session tokens.',
        'options': [
            ('By disabling POST requests', False),
            ('Using the {% csrf_token %} tag and CSRF middleware', True),
            ('By encrypting HTML inputs with base64', False),
            ('By disallowing cookies completely', False),
        ]
    },
    {
        'category': 'django-web-framework',
        'text': 'What default password hashing algorithm is employed by Django Auth? (Slide 10)',
        'marks': 1,
        'explanation': 'Django uses PBKDF2 with SHA256 hashing by default (with optional Argon2 support) and never stores plaintext passwords.',
        'options': [
            ('Plaintext MD5', False),
            ('PBKDF2 with SHA256 / Argon2', True),
            ('ROT13 encoding', False),
            ('Single-round DES', False),
        ]
    },

    # Category 2: Python Core
    {
        'category': 'python-core-concepts',
        'text': 'What is the correct syntax to create a list comprehension of even numbers from 0 to 9 in Python?',
        'marks': 1,
        'explanation': '[x for x in range(10) if x % 2 == 0] generates the list [0, 2, 4, 6, 8].',
        'options': [
            ('[for x in range(10) if x % 2 == 0]', False),
            ('[x for x in range(10) if x % 2 == 0]', True),
            ('{x: x % 2 == 0 for x in range(10)}', False),
            ('(x in range(10) where x % 2 == 0)', False),
        ]
    },
    {
        'category': 'python-core-concepts',
        'text': 'Which built-in Python function returns the memory address of an object?',
        'marks': 1,
        'explanation': 'id(object) returns the identity integer (memory address in CPython).',
        'options': [
            ('loc()', False),
            ('id()', True),
            ('addr()', False),
            ('memory()', False),
        ]
    },
    {
        'category': 'python-core-concepts',
        'text': 'What keyword is used to create a generator function that produces a sequence of values on the fly?',
        'marks': 1,
        'explanation': 'The yield keyword turns a function into a generator, yielding values lazily without storing all items in memory.',
        'options': [
            ('return', False),
            ('yield', True),
            ('emit', False),
            ('produce', False),
        ]
    },
    {
        'category': 'python-core-concepts',
        'text': 'Which of the following data types in Python is immutable?',
        'marks': 1,
        'explanation': 'Tuples are immutable; lists, dictionaries, and sets are mutable.',
        'options': [
            ('List', False),
            ('Dictionary', False),
            ('Tuple', True),
            ('Set', False),
        ]
    },
    {
        'category': 'python-core-concepts',
        'text': 'How do you check if an object is an instance of a specific class or subclass?',
        'marks': 1,
        'explanation': 'isinstance(obj, Class) checks if obj is an instance of Class or a subclass.',
        'options': [
            ('type_of(obj, Class)', False),
            ('isinstance(obj, Class)', True),
            ('obj.has_class(Class)', False),
            ('Class.contains(obj)', False),
        ]
    },

    # Category 3: Web Technologies & Bootstrap 5
    {
        'category': 'web-technologies-bootstrap-5',
        'text': 'How many columns are there in the standard Bootstrap 5 responsive grid system? (Slide 4)',
        'marks': 1,
        'explanation': 'Bootstrap utilizes a 12-column flexbox grid system across various responsive breakpoints.',
        'options': [
            ('8 columns', False),
            ('10 columns', False),
            ('12 columns', True),
            ('16 columns', False),
        ]
    },
    {
        'category': 'web-technologies-bootstrap-5',
        'text': 'Which Bootstrap 5 class makes an HTML button take the full available width of its container?',
        'marks': 1,
        'explanation': 'Using the utility class w-100 or a d-grid wrapper with btn makes a button occupy 100% width.',
        'options': [
            ('btn-block', False),
            ('w-100', True),
            ('btn-full', False),
            ('width-max', False),
        ]
    },
    {
        'category': 'web-technologies-bootstrap-5',
        'text': 'Which semantic HTML5 tag is most appropriate for navigational links?',
        'marks': 1,
        'explanation': 'The <nav> tag represents a section of a page that links to other pages or parts within the page.',
        'options': [
            ('<section>', False),
            ('<nav>', True),
            ('<menu>', False),
            ('<aside>', False),
        ]
    },
    {
        'category': 'web-technologies-bootstrap-5',
        'text': 'What CSS property is primarily used to align flex items along the main axis?',
        'marks': 1,
        'explanation': 'justify-content aligns items along the main axis; align-items aligns along the cross axis.',
        'options': [
            ('align-items', False),
            ('justify-content', True),
            ('flex-flow', False),
            ('content-align', False),
        ]
    },

    # Category 4: Database Systems & SQL
    {
        'category': 'database-systems-sql',
        'text': 'In the QuizSphere database design, which field connects Question to Category? (Slide 7)',
        'marks': 1,
        'explanation': 'category_id (FK) connects the Question table to Category, establishing a One-to-Many relationship.',
        'options': [
            ('Primary Key id', False),
            ('category_id (ForeignKey)', True),
            ('slug string', False),
            ('Many-to-Many intermediary table', False),
        ]
    },
    {
        'category': 'database-systems-sql',
        'text': 'How does the Django ORM protect against SQL Injection attacks? (Slide 10)',
        'marks': 1,
        'explanation': 'Django ORM parameterizes all database queries by default, separating SQL command structure from user input values.',
        'options': [
            ('By blocking all WHERE clauses', False),
            ('By using parameterized queries automatically', True),
            ('By converting SQL to XML', False),
            ('By storing database tables in memory only', False),
        ]
    },
    {
        'category': 'database-systems-sql',
        'text': 'Which database is recommended for QuizSphere development vs production? (Slide 4)',
        'marks': 1,
        'explanation': 'Slide 4 designates SQLite for local development and PostgreSQL for production environments.',
        'options': [
            ('MongoDB for dev / Redis for prod', False),
            ('SQLite (dev) / PostgreSQL (prod)', True),
            ('MS Access for dev / Oracle for prod', False),
            ('MySQL only for all environments', False),
        ]
    }
]

# Wipe old questions to avoid duplicates on re-run
Question.objects.all().delete()

for q_data in questions_data:
    cat = created_categories[q_data['category']]
    q = Question.objects.create(
        category=cat,
        text=q_data['text'],
        marks=q_data['marks'],
        explanation=q_data['explanation']
    )
    for opt_text, is_correct in q_data['options']:
        Option.objects.create(
            question=q,
            text=opt_text,
            is_correct=is_correct
        )

print(f"Total questions created: {Question.objects.count()}")
print(f"Total options created: {Option.objects.count()}")

# 4. Seed realistic attempts & answers for initial Leaderboard & Dashboard
QuizAttempt.objects.all().delete()

seed_attempts = [
    {
        'user': demo1_user,
        'category': created_categories['django-web-framework'],
        'score': 5,
        'total_marks': 5,
        'percentage': 100.0,
        'time_taken': 42,
        'passed': True,
        'offset_days': 1
    },
    {
        'user': demo2_user,
        'category': created_categories['django-web-framework'],
        'score': 4,
        'total_marks': 5,
        'percentage': 80.0,
        'time_taken': 58,
        'passed': True,
        'offset_days': 2
    },
    {
        'user': demo3_user,
        'category': created_categories['python-core-concepts'],
        'score': 5,
        'total_marks': 5,
        'percentage': 100.0,
        'time_taken': 48,
        'passed': True,
        'offset_days': 1
    },
    {
        'user': student_user,
        'category': created_categories['django-web-framework'],
        'score': 4,
        'total_marks': 5,
        'percentage': 80.0,
        'time_taken': 65,
        'passed': True,
        'offset_days': 3
    },
    {
        'user': demo1_user,
        'category': created_categories['database-systems-sql'],
        'score': 3,
        'total_marks': 3,
        'percentage': 100.0,
        'time_taken': 30,
        'passed': True,
        'offset_days': 2
    },
    {
        'user': demo2_user,
        'category': created_categories['web-technologies-bootstrap-5'],
        'score': 4,
        'total_marks': 4,
        'percentage': 100.0,
        'time_taken': 35,
        'passed': True,
        'offset_days': 1
    }
]

for item in seed_attempts:
    attempt = QuizAttempt.objects.create(
        user=item['user'],
        category=item['category'],
        score=item['score'],
        total_marks=item['total_marks'],
        percentage=item['percentage'],
        time_taken_seconds=item['time_taken'],
        passed=item['passed'],
        date_taken=timezone.now() - timedelta(days=item['offset_days'])
    )
    
    # Create matching AttemptAnswer records
    for q in item['category'].questions.all():
        correct_opt = q.options.filter(is_correct=True).first()
        AttemptAnswer.objects.create(
            attempt=attempt,
            question=q,
            selected_option=correct_opt,
            is_correct=True,
            marks_obtained=q.marks
        )

print(f"Seed attempts created: {QuizAttempt.objects.count()}")
print("Seeding finished successfully!")
