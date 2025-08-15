@echo off
echo FullMoon OJ - Docker Production Commands
echo ========================================

REM Check if docker-compose or docker compose is available
docker-compose --version >nul 2>&1
if %errorlevel% equ 0 (
    set COMPOSE_CMD=docker-compose
) else (
    docker compose version >nul 2>&1
    if %errorlevel% equ 0 (
        set COMPOSE_CMD=docker compose
    ) else (
        echo ERROR: Neither docker-compose nor docker compose is available!
        echo Please install Docker Desktop for Windows first.
        echo Download from: https://www.docker.com/products/docker-desktop/
        pause
        exit /b 1
    )
)

echo Using: %COMPOSE_CMD%

if "%1"=="build" goto build
if "%1"=="up" goto up
if "%1"=="down" goto down
if "%1"=="logs" goto logs
if "%1"=="shell" goto shell
if "%1"=="clean" goto clean
if "%1"=="help" goto help

:help
echo.
echo Usage: docker-prod.bat [command]
echo.
echo Commands:
echo   build  - Build production containers
echo   up     - Start production environment
echo   down   - Stop production environment
echo   logs   - View container logs
echo   shell  - Open shell in web container
echo   clean  - Clean up containers and images
echo   help   - Show this help message
echo.
echo Examples:
echo   docker-prod.bat build
echo   docker-prod.bat up
echo   docker-prod.bat logs
echo.
goto end

:build
echo Building production containers...
%COMPOSE_CMD% --profile production build
goto end

:up
echo Starting production environment...
%COMPOSE_CMD% --profile production up -d
echo.
echo Production stack is starting up...
echo Services:
echo   - Django + Gunicorn: http://localhost:8001
echo   - PostgreSQL: localhost:5432
echo   - Redis: localhost:6379
echo   - Nginx: http://localhost (HTTP), https://localhost (HTTPS)
echo.
echo Use 'docker-prod.bat logs' to view logs
goto end

:down
echo Stopping production environment...
%COMPOSE_CMD% --profile production down
goto end

:logs
echo Viewing production logs (Press Ctrl+C to exit)...
%COMPOSE_CMD% --profile production logs -f
goto end

:shell
echo Opening shell in web container...
%COMPOSE_CMD% --profile production exec web-prod bash
goto end

:clean
echo Cleaning up production containers and images...
%COMPOSE_CMD% --profile production down -v --remove-orphans
docker system prune -f
docker volume prune -f
echo Cleanup complete!
goto end

:end
pause
