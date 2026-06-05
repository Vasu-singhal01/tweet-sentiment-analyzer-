@echo off
title Tweet Sentiment Analyzer
color 0A

echo.
echo =====================================================
echo    TWEET SENTIMENT ANALYZER
echo    B.Tech CSE (Data Science) - Bennett University
echo    By: Vasu Singhal
echo =====================================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    pause
    exit
)
echo       Python found!

echo.
echo [2/3] Installing required libraries...
pip install flask vaderSentiment --quiet
echo       Libraries ready!

echo.
echo [3/3] Starting the application...
echo       Browser will open automatically at http://localhost:5000
echo.
echo =====================================================
echo   Press CTRL+C to stop the server
echo =====================================================
echo.

python app.py
pause
