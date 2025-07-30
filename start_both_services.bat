@echo off
echo ========================================
echo Starting AI Travel System
echo ========================================
echo.
echo This will start both the Node.js application and Python AI service
echo.

echo Starting Python AI Service on port 5001...
start "AI Service" cmd /k "cd ai_service && python app.py"

echo Waiting 5 seconds for AI service to start...
timeout /t 5 /nobreak > nul

echo Starting Node.js Application on port 5000...
start "Node.js App" cmd /k "npm start"

echo.
echo ========================================
echo Services Started Successfully!
echo ========================================
echo.
echo Node.js Application: http://localhost:5000
echo Python AI Service: http://localhost:5001
echo.
echo Press any key to close this window...
pause > nul 