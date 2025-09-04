@echo off
cd ..
call venv\Scripts\activate.bat
python export_to_prom.py
pause

