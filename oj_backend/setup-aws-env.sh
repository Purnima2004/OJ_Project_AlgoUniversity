#!/bin/bash

# AWS Environment Setup Script for FullMoon OJ
# This script sets up the necessary environment variables on AWS EC2

echo "🚀 Setting up AWS environment for FullMoon OJ..."

# Create .env file with production settings
cat > .env << EOF
# Django Settings
SECRET_KEY=django-insecure-gh42c=oebk5h-wf2@m_vwe+dtef9kb#ck#6nv%@w4a!9vxm*_%
DEBUG=False
IS_PRODUCTION=True

# Database Settings (SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Google AI API Key - REPLACE WITH YOUR ACTUAL API KEY
GOOGLE_API_KEY=your_google_api_key_here

# AWS Settings
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_S3_REGION_NAME=ap-south-1

# Allowed Hosts
ALLOWED_HOSTS=13.234.242.181,fullmoon.icu,www.fullmoon.icu,localhost,127.0.0.1

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://fullmoon.icu,https://www.fullmoon.icu,http://13.234.242.181,http://fullmoon.icu,http://www.fullmoon.icu
EOF

echo "✅ Created .env file"

# Set environment variables in current session
export SECRET_KEY="django-insecure-gh42c=oebk5h-wf2@m_vwe+dtef9kb#ck#6nv%@w4a!9vxm*_%"
export DEBUG="False"
export IS_PRODUCTION="True"

echo "✅ Set environment variables in current session"

# Make .env file executable
chmod 600 .env

echo "🔒 Set proper permissions for .env file"

# Instructions for the user
echo ""
echo "📝 IMPORTANT: You need to edit the .env file and add your actual Google API key!"
echo "   Edit the GOOGLE_API_KEY line in the .env file:"
echo "   GOOGLE_API_KEY=your_actual_api_key_here"
echo ""
echo "🔑 To get your Google API key:"
echo "   1. Go to https://makersuite.google.com/app/apikey"
echo "   2. Create a new API key"
echo "   3. Copy the key and replace 'your_google_api_key_here' in .env"
echo ""
echo "🚀 After updating the API key, restart your Django server:"
echo "   sudo systemctl restart gunicorn"
echo "   # or if running manually:"
echo "   python manage.py runserver 0.0.0.0:8000"
echo ""
echo "✅ Environment setup complete!"
















