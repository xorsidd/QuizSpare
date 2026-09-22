/**
 * QuizSphere Main Interactive Engine
 * Handles countdown timer, auto-submission, question palette, MVT diagram interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 6000);
    });

    // 2. Interactive Quiz Engine
    initQuizEngine();

    // 3. MVT Architecture Interactive Explorer
    initMvtExplorer();
});

function initQuizEngine() {
    const quizForm = document.getElementById('quiz-attempt-form');
    if (!quizForm) return;

    const timerDisplay = document.getElementById('quiz-timer');
    const timeTakenInput = document.getElementById('time_taken_seconds');
    let totalSeconds = parseInt(quizForm.dataset.timeLimit || '600', 10);
    let secondsLeft = totalSeconds;
    let elapsedSeconds = 0;

    // Format mm:ss
    function formatTime(s) {
        const mins = Math.floor(s / 60);
        const secs = s % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    if (timerDisplay) {
        timerDisplay.textContent = formatTime(secondsLeft);

        const timerInterval = setInterval(() => {
            secondsLeft--;
            elapsedSeconds++;
            if (timeTakenInput) {
                timeTakenInput.value = elapsedSeconds;
            }

            if (secondsLeft <= 0) {
                clearInterval(timerInterval);
                timerDisplay.textContent = "00:00";
                timerDisplay.parentElement.classList.add('timer-urgent');
                // Auto submit!
                alert("⏰ Time is up! Your answers are being submitted automatically.");
                quizForm.submit();
                return;
            }

            timerDisplay.textContent = formatTime(secondsLeft);

            // Warning under 60 seconds
            if (secondsLeft <= 60) {
                timerDisplay.parentElement.classList.add('timer-urgent');
            }
        }, 1000);
    }

    // Palette tracking
    const questionCards = document.querySelectorAll('.question-card');
    const paletteButtons = document.querySelectorAll('.question-nav-btn');
    const answeredCountEl = document.getElementById('answered-count');

    function updateAnsweredCount() {
        let count = 0;
        questionCards.forEach(card => {
            const qId = card.dataset.questionId;
            const checked = card.querySelector(`input[name="question_${qId}"]:checked`);
            const navBtn = document.querySelector(`.question-nav-btn[data-q-idx="${card.dataset.qIndex}"]`);
            if (checked) {
                count++;
                if (navBtn) navBtn.classList.add('answered');
            } else {
                if (navBtn) navBtn.classList.remove('answered');
            }
        });
        if (answeredCountEl) {
            answeredCountEl.textContent = count;
        }
    }

    // Listen to radio changes
    quizForm.querySelectorAll('input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', updateAnsweredCount);
    });

    // Question jump buttons
    paletteButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = btn.getAttribute('href');
            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                // Highlight target temporarily
                targetEl.classList.add('shadow-lg');
                setTimeout(() => targetEl.classList.remove('shadow-lg'), 1200);
            }
        });
    });

    // Initial check
    updateAnsweredCount();
}

function initMvtExplorer() {
    const mvtNodes = document.querySelectorAll('.mvt-node');
    const descBox = document.getElementById('mvt-detail-box');
    if (!descBox || !mvtNodes.length) return;

    const details = {
        'browser': {
            title: '1. Browser (Client Request)',
            desc: 'The user visits a URL (e.g. /quiz/django-framework/start/). The browser sends an HTTP GET or POST request to the Django web server.',
            file: 'Client HTTP Request',
            code: 'GET /quiz/python/start/ HTTP/1.1\nHost: quizsphere.local'
        },
        'urls': {
            title: '2. URL Dispatcher (urls.py)',
            desc: 'Django inspects the incoming request path and matches it against urlpatterns. It routes the request to the matching view function.',
            file: 'quiz/urls.py',
            code: 'urlpatterns = [\n    path("quiz/<slug:slug>/start/", views.quiz_take, name="quiz_take"),\n]'
        },
        'views': {
            title: '3. View (views.py) - Business Logic',
            desc: 'The view handles user authentication, session state, timer calculations, and calls the Model via Django ORM to fetch data.',
            file: 'quiz/views.py',
            code: '@login_required\ndef quiz_take(request, slug):\n    category = get_object_or_404(Category, slug=slug)\n    questions = category.questions.prefetch_related("options").all()\n    return render(request, "quiz/quiz_take.html", context)'
        },
        'models': {
            title: '4. Model (models.py) & Django ORM',
            desc: 'Defines the schema (Category, Question, Option, QuizAttempt) with ForeignKeys. Django ORM translates Python queries to safe parameterized SQL.',
            file: 'quiz/models.py',
            code: 'class Question(models.Model):\n    category = models.ForeignKey(Category, on_delete=models.CASCADE)\n    text = models.TextField()\n    marks = models.PositiveIntegerField(default=1)'
        },
        'database': {
            title: '5. Database (SQLite / PostgreSQL)',
            desc: 'Executes the SQL queries efficiently. Stores relational tables for users, categories, options, attempts, and answers.',
            file: 'db.sqlite3 / PostgreSQL',
            code: 'SELECT "quiz_question"."id", "quiz_question"."text" FROM "quiz_question" WHERE category_id = 1;'
        },
        'templates': {
            title: '6. Template (Django Template Engine - DTL)',
            desc: 'Merges the context data from the view with HTML5/Bootstrap5 templates to generate the responsive response page sent back to the browser.',
            file: 'templates/quiz/quiz_take.html',
            code: '{% for question in questions %}\n  <div class="card mb-3">\n    <h5>{{ forloop.counter }}. {{ question.text }}</h5>\n  </div>\n{% endfor %}'
        }
    };

    mvtNodes.forEach(node => {
        node.addEventListener('click', () => {
            mvtNodes.forEach(n => n.classList.remove('active-node'));
            node.classList.add('active-node');
            const key = node.dataset.node;
            const data = details[key];
            if (data) {
                descBox.innerHTML = `
                    <div class="card border-primary shadow-sm">
                        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                            <strong>${data.title}</strong>
                            <span class="badge bg-light text-primary font-mono">${data.file}</span>
                        </div>
                        <div class="card-body">
                            <p class="card-text fs-6">${data.desc}</p>
                            <h6 class="fw-bold small text-muted text-uppercase mt-3">Code / Flow snippet:</h6>
                            <pre class="bg-dark text-light p-3 rounded-3 font-mono small mb-0"><code>${escapeHtml(data.code)}</code></pre>
                        </div>
                    </div>
                `;
            }
        });
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.innerText = text;
    return div.innerHTML;
}
