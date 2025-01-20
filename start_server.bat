@echo off
cd /d "C:\Users\pc\Documents\ruiz_clinic"
call venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
pause
