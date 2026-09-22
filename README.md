# QuizSphere — Student Online Quiz Platform
### A Full-Stack Django + Python Web Application (Student Focused)

**Based on:** `QuizSphere_Final.pptx`  
**Django Mini Project Presentation**  
**Presented by:**
- **Demo Student 1** (Roll No: `DEMO01`)
- **Demo Student 2** (Roll No: `DEMO02`)
- **Demo Student 3** (Roll No: `DEMO03`)

---

## 🎯 Clean, Tiny Student-Only Architecture

QuizSphere has been streamlined for students with a focus on ease-of-use and learning retention:
- **Fast Student Registration & Sign In**: No complex admin setup; learners sign up directly and start testing.
- **Subject Categories**: Choose from Django Framework, Python Core, Web Technologies & Bootstrap 5, and Database Systems.
- **Live Timed Examinations**: Real-time countdown timer bar per quiz with automatic submission when time hits `00:00`.
- **Question Navigator**: Interactive palette tracking answered vs unanswered questions.
- **Instant Auto-Grading**: Millisecond grading on submission with pass/fail threshold check.
- **Detailed Question Audit Review**: Visual review showing correct answers (green) and incorrect choices (red) with technical explanations.
- **Competitive Leaderboard**: Global and subject-wise rankings with 🥇 Gold, 🥈 Silver, and 🥉 Bronze medals.
- **Personal Student Dashboard**: Track total quizzes taken, passed assessments, pass rate percentage, and attempt history.
- **Presentation & Architecture Showcase**: Full 12-slide walkthrough and interactive Django MVT architecture diagram.

---

## 🚦 How to Launch the Web App

Double-click **`run_quizsphere.bat`**, or run in terminal:
```bash
# 1. (Optional) Run migrations if setting up fresh database:
python manage.py migrate

# 2. (Optional) Populate seed questions and demo data:
python seed_data.py

# 3. Start the development server:
python manage.py runserver 127.0.0.1:8000
```
Open **`http://127.0.0.1:8000/`** in your browser.

**Demo Credentials:**
- Student: `username: student` | `password: student123`
- Admin: `username: admin` | `password: admin123`
