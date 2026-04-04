@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo   OJ Backend - AWS EC2 Upload Helper
echo ===================================================

:: Prompt for details
set /p EC2_IP="Enter EC2 Public IP Address: "
set /p KEY_PATH="Enter full path to your .pem key file: "

:: Verify key file exists
if not exist "!KEY_PATH!" (
    echo Error: Key file not found at "!KEY_PATH!"
    pause
    exit /b 1
)

:: Check if tar file exists
if not exist "fullmoon-oj-backend.tar" (
    echo Error: fullmoon-oj-backend.tar not found!
    echo Please wait for the Docker build and save process to complete.
    pause
    exit /b 1
)

echo.
echo [1/2] Uploading Docker image to EC2...
echo This may take a while depending on your upload speed...
scp -i "!KEY_PATH!" fullmoon-oj-backend.tar ubuntu@!EC2_IP!:~

if !errorlevel! neq 0 (
    echo.
    echo [ERROR] Upload failed. Please check your IP and Key.
    pause
    exit /b 1
)

echo.
echo [2/2] Loading image on EC2...
ssh -i "!KEY_PATH!" ubuntu@!EC2_IP! "echo 'Loading image...' && docker load -i fullmoon-oj-backend.tar"

if !errorlevel! neq 0 (
    echo.
    echo [ERROR] Failed to load image on remote server.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo   SUCCESS! Image uploaded and loaded.
echo ===================================================
echo.
echo To start the container, run:
echo ssh -i "!KEY_PATH!" ubuntu@!EC2_IP! "docker run -d -p 8000:8000 --env-file .env fullmoon-oj-backend"
echo.
pause
