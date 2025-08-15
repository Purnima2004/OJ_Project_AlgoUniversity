@echo off
echo FullMoon OJ - Docker Development Commands
echo =========================================

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
echo Usage: docker-dev.bat [command]
echo.
echo Commands:
echo   build  - Build development container
echo   up     - Start development environment
echo   down   - Stop development environment
echo   logs   - View container logs
echo   shell  - Open shell in container
echo   clean  - Clean up containers and images
echo   help   - Show this help message
echo.
echo Examples:
echo   docker-dev.bat build
echo   docker-dev.bat up
echo   docker-dev.bat logs
echo.
goto end

:build
echo Building development container...
%COMPOSE_CMD% -f docker-compose.dev.yml build
goto end

:up
echo Starting development environment...
%COMPOSE_CMD% -f docker-compose.dev.yml up -d
echo.
echo FullMoon OJ is starting up...
echo Wait a few moments, then visit: http://localhost:8000
echo Use 'docker-dev.bat logs' to view logs
goto end

:down
echo Stopping development environment...
%COMPOSE_CMD% -f docker-compose.dev.yml down
goto end

:logs
echo Viewing container logs (Press Ctrl+C to exit)...
%COMPOSE_CMD% -f docker-compose.dev.yml logs -f
goto end

:shell
echo Opening shell in container...
%COMPOSE_CMD% -f docker-compose.dev.yml exec web bash
goto end

:clean
echo Cleaning up containers and images...
%COMPOSE_CMD% -f docker-compose.dev.yml down -v --remove-orphans
docker system prune -f
docker volume prune -f
echo Cleanup complete!
goto end

:end
pause
