@echo off
echo.
echo [INFO] Installing admin web dependencies...
echo.

cd /d "%~dp0"
cd ..
npm install --registry=https://registry.npmmirror.com

pause
