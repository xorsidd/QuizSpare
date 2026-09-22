@echo off
title QuizSphere - Online Quiz & Assessment Platform
echo =====================================================================
echo   QuizSphere: An Interactive Online Quiz & Assessment Platform
echo   A DJANGO + PYTHON WEB APPLICATION
echo   Presented by: Demo Student 1 (DEMO01), Demo Student 2 (DEMO02), Demo Student 3 (DEMO03)
echo =====================================================================
echo.
echo Starting Django Development Server on http://127.0.0.1:8000/ ...
echo.
echo Default Demo Logins:
echo   - Admin:   username: admin    password: admin123
echo   - Student: username: student  password: student123
echo.
cd /d "%~dp0"
python manage.py runserver 127.0.0.1:8000
if %errorlevel% neq 0 (
    py manage.py runserver 127.0.0.1:8000
)
pause
