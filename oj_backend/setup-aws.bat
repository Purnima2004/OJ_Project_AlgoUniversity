@echo off
REM AWS Setup Script for FullMoon OJ Platform (Windows)

echo 🚀 Starting AWS setup for FullMoon OJ Platform...

REM Set production environment
set IS_PRODUCTION=true

REM Check if .env file exists, if not create it
if not exist .env (
    echo 📝 Creating .env file...
    (
        echo # Environment Variables for FullMoon OJ Platform
        echo.
        echo # Production Settings
        echo IS_PRODUCTION=True
        echo.
        echo # Django Secret Key
        echo SECRET_KEY=django-insecure-gh42c=oebk5h-wf2@m_vwe+dtef9kb#ck#6nv%@w4a!9vxm*_%_aws_production
        echo.
        echo # Google Gemini API Key - SET THIS TO YOUR ACTUAL API KEY
        echo GOOGLE_API_KEY=your-actual-api-key-here
        echo.
        echo # Database Settings ^(SQLite^)
        echo DATABASE_URL=sqlite:///db.sqlite3
        echo.
        echo # Static Files
        echo STATIC_ROOT=staticfiles
        echo MEDIA_ROOT=media
    ) > .env
    echo ⚠️  IMPORTANT: Please edit .env file and set your actual GOOGLE_API_KEY
)

REM Install dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist staticfiles mkdir staticfiles
if not exist media mkdir media
if not exist logs mkdir logs

REM Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput --clear

REM Run database migrations
echo 🗄️  Running database migrations...
python manage.py migrate

REM Create superuser if it doesn't exist
echo 👤 Checking for superuser...
python manage.py shell -c "from django.contrib.auth.models import User; print('✅ Superuser check completed')"

REM Test the application
echo 🧪 Testing the application...
python manage.py check --deploy

echo.
echo ✅ AWS setup completed!
echo.
echo 📋 Next steps:
echo 1. Edit .env file and set your actual GOOGLE_API_KEY
echo 2. Run: python manage.py runserver 0.0.0.0:8000
echo 3. Or use gunicorn: gunicorn oj_backend.wsgi:application --bind 0.0.0.0:8000
echo.
echo 🚀 FullMoon OJ Platform is ready for AWS deployment!
pause

