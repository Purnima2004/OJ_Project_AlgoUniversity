@echo off
echo FullMoon OJ - Simple Docker Commands
echo =====================================

if "%1"=="build" (
    echo Building Docker image...
    docker-compose -f docker-compose.simple.yml build
) else if "%1"=="up" (
    echo Starting container...
    docker-compose -f docker-compose.simple.yml up
) else if "%1"=="down" (
    echo Stopping container...
    docker-compose -f docker-compose.simple.yml down
) else if "%1"=="logs" (
    echo Showing logs...
    docker-compose -f docker-compose.simple.yml logs -f
) else if "%1"=="shell" (
    echo Opening shell in container...
    docker-compose -f docker-compose.simple.yml exec web bash
) else if "%1"=="clean" (
    echo Cleaning up...
    docker-compose -f docker-compose.simple.yml down
    docker system prune -f
) else (
    echo Usage: docker-simple.bat [build^|up^|down^|logs^|shell^|clean]
    echo.
    echo Commands:
    echo   build  - Build the Docker image
    echo   up     - Start the container
    echo   down   - Stop the container
    echo   logs   - Show container logs
    echo   shell  - Open shell in container
    echo   clean  - Clean up Docker resources
)
