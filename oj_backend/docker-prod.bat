@echo off
echo FullMoon OJ - Production Docker Commands
echo =========================================

if "%1"=="build" (
    echo Building Production Docker image...
    docker-compose -f docker-compose.prod.yml build
) else if "%1"=="up" (
    echo Starting Production container...
    docker-compose -f docker-compose.prod.yml up -d
) else if "%1"=="down" (
    echo Stopping Production container...
    docker-compose -f docker-compose.prod.yml down
) else if "%1"=="logs" (
    echo Showing Production logs...
    docker-compose -f docker-compose.prod.yml logs -f
) else if "%1"=="restart" (
    echo Restarting Production container...
    docker-compose -f docker-compose.prod.yml restart
) else if "%1"=="status" (
    echo Checking Production container status...
    docker-compose -f docker-compose.prod.yml ps
) else if "%1"=="clean" (
    echo Cleaning up Production resources...
    docker-compose -f docker-compose.prod.yml down
    docker system prune -f
) else (
    echo Usage: docker-prod.bat [build^|up^|down^|logs^|restart^|status^|clean]
    echo.
    echo Commands:
    echo   build   - Build the Production Docker image
    echo   up      - Start the Production container (detached)
    echo   down    - Stop the Production container
    echo   logs    - Show Production container logs
    echo   restart - Restart the Production container
    echo   status  - Check container status
    echo   clean   - Clean up Docker resources
)
