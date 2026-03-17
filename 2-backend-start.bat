@echo off
setlocal

cd /d "%~dp0"
call "ruoyi-fastapi-backend\run.bat" %*

