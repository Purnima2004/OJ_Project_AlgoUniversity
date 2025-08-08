@echo off
echo Starting daily content update...
cd /d "%~dp0"
python manage.py update_concept_of_day
python manage.py update_contests
echo Daily content update completed!
pause 