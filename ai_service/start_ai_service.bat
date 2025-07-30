@echo off
echo Starting AI Travel Service...
echo.
echo Make sure you have Python installed and dependencies installed
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting AI service on port 5001...
python app.py
pause 