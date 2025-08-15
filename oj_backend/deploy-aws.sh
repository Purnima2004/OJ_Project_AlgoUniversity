#!/bin/bash

# FullMoon OJ - AWS Deployment Script
echo "🚀 Starting FullMoon OJ AWS Deployment..."

# Check if .env.aws exists
if [ ! -f .env.aws ]; then
    echo "❌ Error: .env.aws file not found!"
    echo "Please copy env.aws.example to .env.aws and fill in your values"
    exit 1
fi

# Load environment variables
source .env.aws

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p codes
mkdir -p media

# Set permissions
echo "🔐 Setting permissions..."
chmod 755 logs codes media

# Build and start containers
echo "🔨 Building Docker image..."
docker-compose -f docker-compose.aws.yml build

echo "🚀 Starting containers..."
docker-compose -f docker-compose.aws.yml up -d

# Wait for container to be ready
echo "⏳ Waiting for container to be ready..."
sleep 30

# Check container status
echo "📊 Checking container status..."
docker-compose -f docker-compose.aws.yml ps

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose -f docker-compose.aws.yml exec web python manage.py migrate --settings=oj_backend.settings_aws

# Create superuser (optional)
echo "👤 Creating superuser..."
docker-compose -f docker-compose.aws.yml exec web python manage.py createsuperuser --settings=oj_backend.settings_aws

echo "✅ Deployment completed successfully!"
echo "🌐 Your FullMoon OJ is now running on AWS!"
echo "🔗 Access it at: http://your-ec2-public-ip:8000"
