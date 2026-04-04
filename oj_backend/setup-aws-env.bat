@echo off
REM AWS Environment Setup Script for FullMoon OJ (Windows)
REM This script sets up the necessary environment variables for AWS deployment

echo 🚀 Setting up AWS environment for FullMoon OJ...

REM Create .env file with production settings
(
echo # Django Settings
echo SECRET_KEY=django-insecure-gh42c=oebk5h-wf2@m_vwe+dtef9kb#ck#6nv%%w4a!9vxm*_%%
echo DEBUG=False
echo IS_PRODUCTION=True
echo.
echo # Database Settings (SQLite)
echo DATABASE_URL=sqlite:///db.sqlite3
echo.
echo # Google AI API Key - REPLACE WITH YOUR ACTUAL API KEY
echo GOOGLE_API_KEY=your_google_api_key_here
echo.
echo # AWS Settings
echo AWS_ACCESS_KEY_ID=your_aws_access_key
echo AWS_SECRET_ACCESS_KEY=your_aws_secret_key
echo AWS_STORAGE_BUCKET_NAME=your_bucket_name
echo AWS_S3_REGION_NAME=ap-south-1
echo.
echo # Allowed Hosts
echo ALLOWED_HOSTS=13.234.242.181,fullmoon.icu,www.fullmoon.icu,localhost,127.0.0.1
echo.
echo # CSRF Trusted Origins
echo CSRF_TRUSTED_ORIGINS=https://fullmoon.icu,https://www.fullmoon.icu,http://13.234.242.181,http://fullmoon.icu,http://www.fullmoon.icu
) > .env

echo ✅ Created .env file

REM Set environment variables in current session
set SECRET_KEY=django-insecure-gh42c=oebk5h-wf2@m_vwe+dtef9kb#ck#6nv%%w4a!9vxm*_%%
set DEBUG=False
set IS_PRODUCTION=True

echo ✅ Set environment variables in current session

echo.
echo 📝 IMPORTANT: You need to edit the .env file and add your actual Google API key!
echo    Edit the GOOGLE_API_KEY line in the .env file:
echo    GOOGLE_API_KEY=your_actual_api_key_here
echo.
echo 🔑 To get your Google API key:
echo    1. Go to https://makersuite.google.com/app/apikey
echo    2. Create a new API key
echo    3. Copy the key and replace 'your_google_api_key_here' in .env
echo.
echo 🚀 After updating the API key, restart your Django server:
echo    python manage.py runserver
echo.
echo ✅ Environment setup complete!
pause
















