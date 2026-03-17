@echo off
setlocal

cd /d "%~dp0"

set "RUN_ENV=%~1"
if "%RUN_ENV%"=="" set "RUN_ENV=dev"
set "ENV_FILE=.env.%RUN_ENV%"
set "PYTHON_BIN=.venv\Scripts\python.exe"

if not exist "%ENV_FILE%" (
  echo [ERROR] Missing env file: %CD%\%ENV_FILE%
  echo [TIP] Local development uses .env.dev by default.
  echo [TIP] For deployment, create the matching .env.NAME file first.
  exit /b 1
)

if not exist "%PYTHON_BIN%" (
  echo [ERROR] Missing virtualenv python: %CD%\%PYTHON_BIN%
  echo [TIP] Run these commands in ruoyi-fastapi-backend first:
  echo        python -m venv .venv
  echo        .venv\Scripts\python.exe -m pip install -r requirements.txt
  exit /b 1
)

echo [DeskOps Backend] Workdir: %CD%
echo [DeskOps Backend] APP_ENV=%RUN_ENV%
echo [DeskOps Backend] ENV_FILE=%CD%\%ENV_FILE%
echo [DeskOps Backend] Command: %PYTHON_BIN% app.py --env %RUN_ENV%
echo.

"%PYTHON_BIN%" app.py --env "%RUN_ENV%"
