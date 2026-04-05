@echo off
echo Starting Taste Hub Server...

:: Start the python server
start python app.py

:: Wait for a couple of seconds to ensure the server is fully up
timeout /t 3 /nobreak > nul

:: Open the browser
echo Opening the application...
start http://127.0.0.1:5000

echo To stop the server later, close the newly opened command line window.
pause
