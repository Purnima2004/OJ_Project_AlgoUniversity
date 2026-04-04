#!/bin/bash

# AWS Deployment Script for FullMoon OJ Platform
# This script sets up the environment and deploys the application

echo "🚀 Starting AWS deployment for FullMoon OJ Platform..."

# Set production environment
export IS_PRODUCTION=true

# Check if .env file exists, if not create from example
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cat > .env << EOF
# Environment Variables for FullMoon OJ Platform

# Production Settings
IS_PRODUCTION=True

# Django Secret Key (generate a new one for production)
SECRET_KEY=django-insecure-gh42c=oebk5h-wf2@m_vwe+dtef9kb#ck#6nv%@w4a!9vxm*_%_aws_production

# Google Gemini API Key - SET THIS TO YOUR ACTUAL API KEY
GOOGLE_API_KEY=your-actual-api-key-here

# Database Settings (SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Static Files
STATIC_ROOT=staticfiles
MEDIA_ROOT=media
EOF
    echo "⚠️  IMPORTANT: Please edit .env file and set your actual GOOGLE_API_KEY"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p staticfiles
mkdir -p media
mkdir -p logs

# Set proper permissions
echo "🔐 Setting proper permissions..."
chmod 755 staticfiles
chmod 755 media
chmod 644 .env

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fullmoon.icu', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
"

# Create sample data if database is empty
echo "📊 Creating sample data..."
python manage.py shell -c "
from auth_app.models import Problem, Contest, ConceptOfDay
if Problem.objects.count() == 0:
    print('📝 Creating sample problems...')
    exec(open('auth_app/management/commands/create_sample_data.py').read())
else:
    print('✅ Sample data already exists')
"

# Set production environment variables
echo "🌍 Setting production environment..."
export DJANGO_SETTINGS_MODULE=oj_backend.settings
export IS_PRODUCTION=true

# Test the application
echo "🧪 Testing the application..."
python manage.py check --deploy

echo "✅ Deployment setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file and set your actual GOOGLE_API_KEY"
echo "2. Run: python manage.py runserver 0.0.0.0:8000"
echo "3. Or use gunicorn: gunicorn oj_backend.wsgi:application --bind 0.0.0.0:8000"
echo ""
echo "🔍 To check logs: tail -f django.log"
echo "🗄️  To access database: python manage.py dbshell"
echo ""
echo "🚀 FullMoon OJ Platform is ready for AWS deployment!"
