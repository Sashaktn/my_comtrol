@echo off
REM Запуск бекенду FastAPI
start cmd /k "cd /d %~dp0 && venv\Scripts\activate && uvicorn main:app --reload"
REM Запуск фронтенду React
start cmd /k "cd /d %~dp0\frontend && npm start"

