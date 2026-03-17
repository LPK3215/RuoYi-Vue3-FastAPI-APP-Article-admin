@echo off
echo.
echo [INFO] Building admin web app...
echo.

cd /d "%~dp0"
cd ..
npm run build:prod

pause
