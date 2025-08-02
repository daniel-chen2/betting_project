@echo off
REM Navigate to the directory containing your project and venv
cd "C:\Dev\Betting project\Code\betting_project-1"

REM Activate the virtual environment
call betting_project_venv\Scripts\activate.bat

REM Run your Python script
python script.py

REM Deactivate the virtual environment (optional, but good practice)
call deactivate.bat