@echo off
echo.
echo [INFO] Starting admin web dev server...
echo.

cd /d "%~dp0"
cd ..
npm run dev

pause
