# Docker Setup for OJ Project

This directory contains Docker configuration files for running the Online Judge (OJ) project in containers.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (usually comes with Docker Desktop)

## Files Overview

- **Dockerfile** - Single Docker image for development and production
- **docker-compose.yml** - Docker Compose configuration
- **.dockerignore** - Files to exclude from Docker build context

## Quick Start

### Start the Application

```bash
# Build and start the container
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

This will:
- Build the Docker image
- Start the container with Django development server
- Mount your local code for live development
- Run on port 8000

### Stop the Application

```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Database

The project uses **SQLite** database (`db.sqlite3`). The database file is stored in a Docker volume (`sqlite_volume`) to persist data between container restarts.

## Volumes

- **static_volume** - Static files (CSS, JS, images)
- **media_volume** - User-uploaded media files
- **sqlite_volume** - SQLite database file

## Ports

The application runs on port **8000** by default. You can access it at:
- http://localhost:8000

## Environment Variables

- `DEBUG` - Set to `True` for development
- `DJANGO_SETTINGS_MODULE` - Django settings module (defaults to `oj_backend.settings`)

## Useful Commands

### View Logs
```bash
docker-compose logs -f
```

### Access Container Shell
```bash
docker-compose exec web bash
```

### Run Django Commands
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

### Production Mode
For production, you can override the command to use Gunicorn:

```bash
# Run with Gunicorn for production
docker-compose exec web gunicorn --bind 0.0.0.0:8000 oj_backend.wsgi:application
```

## Development Workflow

1. **Start environment**: `docker-compose up --build`
2. **Make code changes** - They will automatically reload
3. **View logs** in the terminal or use `docker-compose logs -f`
4. **Stop environment**: `Ctrl+C` or `docker-compose down`

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, modify the port mapping in docker-compose.yml:
```yaml
ports:
  - "8001:8000"  # Change 8001 to any available port
```

### Database Issues
If you encounter database issues:
```bash
# Remove volumes and recreate
docker-compose down -v
docker volume prune
docker-compose up --build
```

### Clean Build
For a completely fresh start:
```bash
docker-compose down
docker system prune -f
docker-compose up --build
```

## Customization

### Change Port
Edit `docker-compose.yml`:
```yaml
ports:
  - "YOUR_PORT:8000"
```

### Use Gunicorn for Production
Edit `docker-compose.yml`:
```yaml
command: gunicorn --bind 0.0.0.0:8000 oj_backend.wsgi:application
```

### Add Environment Variables
Edit `docker-compose.yml`:
```yaml
environment:
  - DEBUG=False
  - SECRET_KEY=your_secret_key
```

## Why This Simple Setup?

- **Single Dockerfile**: Works for both development and production
- **Single docker-compose.yml**: Easy to manage and understand
- **Flexible**: Can easily switch between development server and production server
- **Maintainable**: Less files to manage and update
