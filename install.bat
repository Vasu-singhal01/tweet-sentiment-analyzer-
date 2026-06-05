@echo off
title Installing Dependencies
color 0E

echo.
echo =====================================================
echo    Installing all required libraries...
echo    This only needs to be done ONCE
echo =====================================================
echo.

pip install flask vaderSentiment pandas numpy matplotlib seaborn scikit-learn jupyter notebook

echo.
echo =====================================================
echo    All libraries installed successfully!
echo    Now you can run:
echo      run.bat          - to launch the web app
echo      open_notebook.bat - to open Jupyter notebook
echo =====================================================
echo.
pause
