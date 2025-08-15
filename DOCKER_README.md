# FullMoon OJ - Docker Setup Guide

This guide explains how to dockerize and deploy your FullMoon Online Judge (OJ) system.

## 🐳 Docker Files Overview

- **`Dockerfile`** - Development container with Django development server
- **`Dockerfile.prod`** - Production container with Gunicorn
- **`docker-compose.yml`** - Complete production stack (Django + PostgreSQL + Redis + Nginx)
- **`docker-compose.dev.yml`** - Development-only setup with SQLite
- **`nginx.conf`** - Nginx configuration for production
- **`settings_prod.py`** - Production Django settings

## 🚀 Quick Start (Development)

### 1. Build and Run Development Container

```bash
# Build the development container
docker-compose -f docker-compose.dev.yml build

# Run the development container
docker-compose -f docker-compose.dev.yml up

# Access your application at: http://localhost:8000
```

### 2. Development with Live Code Changes

The development setup mounts your local `oj_backend/` directory, so code changes are reflected immediately without rebuilding.

## 🏭 Production Deployment

### 1. Environment Setup

```bash
# Copy and edit environment variables
cp env.example .env
nano .env

# Set your production values:
# - SECRET_KEY (generate a strong key)
# - GOOGLE_API_KEY (for AI review feature)
# - Database credentials
# - Email settings
```

### 2. Generate SSL Certificates (Optional)

```bash
# Create SSL directory
mkdir -p ssl

# Generate self-signed certificates (for testing)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem -out ssl/cert.pem

# For production, use Let's Encrypt or your CA
```

### 3. Deploy Production Stack

```bash
# Build and run production services
docker-compose --profile production up -d

# This will start:
# - Django with Gunicorn (port 8001)
# - PostgreSQL database (port 5432)
# - Redis cache (port 6379)
# - Nginx reverse proxy (ports 80, 443)
```

### 4. Initialize Database

```bash
# Create database tables
docker-compose exec web-prod python manage.py migrate

# Create superuser
docker-compose exec web-prod python manage.py createsuperuser

# Load sample data
docker-compose exec web-prod python manage.py setup_sample_data
```

## 🔧 Configuration Options

### Database Configuration

The production setup uses PostgreSQL. To use MySQL instead:

```yaml
# In docker-compose.yml, replace the db service:
db:
  image: mysql:8.0
  environment:
    MYSQL_DATABASE: fullmoon_oj
    MYSQL_USER: fullmoon_user
    MYSQL_PASSWORD: fullmoon_password
    MYSQL_ROOT_PASSWORD: root_password
```

### Scaling

```bash
# Scale Django workers
docker-compose --profile production up -d --scale web-prod=3

# Scale with load balancer
docker-compose --profile production up -d --scale web-prod=5
```

## 📊 Monitoring and Logs

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web-prod
docker-compose logs -f nginx
docker-compose logs -f db
```

### Health Checks

```bash
# Application health
curl http://localhost/health/

# Container health
docker-compose ps
```

## 🛠️ Management Commands

### Database Operations

```bash
# Backup database
docker-compose exec db pg_dump -U fullmoon_user fullmoon_oj > backup.sql

# Restore database
docker-compose exec -T db psql -U fullmoon_user fullmoon_oj < backup.sql

# Reset database
docker-compose exec web-prod python manage.py flush
```

### Static Files

```bash
# Collect static files
docker-compose exec web-prod python manage.py collectstatic --noinput

# Clear static files
docker-compose exec web-prod python manage.py collectstatic --clear --noinput
```

## 🔒 Security Considerations

### Production Checklist

- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use strong database passwords
- [ ] Enable HTTPS with valid SSL certificates
- [ ] Configure firewall rules
- [ ] Set up regular backups
- [ ] Monitor logs for suspicious activity

### Environment Variables

Never commit sensitive information to version control. Use environment variables for:

- Database credentials
- API keys
- Secret keys
- Email settings
- SSL certificates

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Kill the process or change ports in docker-compose.yml
   ```

2. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose exec db pg_isready
   
   # View database logs
   docker-compose logs db
   ```

3. **Permission Issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER oj_backend/
   chmod -R 755 oj_backend/
   ```

4. **Memory Issues**
   ```bash
   # Check container resource usage
   docker stats
   
   # Increase memory limits in docker-compose.yml
   ```

### Performance Tuning

```yaml
# In docker-compose.yml, add resource limits:
web-prod:
  deploy:
    resources:
      limits:
        memory: 1G
        cpus: '0.5'
      reservations:
        memory: 512M
        cpus: '0.25'
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)

## 🤝 Support

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify environment variables
3. Check container status: `docker-compose ps`
4. Ensure all required ports are available
5. Verify SSL certificates (if using HTTPS)

---

**Happy Coding with FullMoon OJ! 🌙**
