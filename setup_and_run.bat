@echo off
REM Setup and Run Script for Speech Therapy Platform

echo ================================================
echo AI Speech Therapy Platform - Setup and Run
echo ================================================
echo.

REM Check if virtual environment exists
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
echo This may take a few minutes on first run...
echo.

python -m pip install --upgrade pip
python -m pip install -r requirements_minimal.txt
python -m pip install nltk

REM Download NLTK data
echo.
echo Downloading NLTK data...
python download_nltk_data.py

REM Check installation
echo.
echo Verifying installation...
python -c "import streamlit; import librosa; print('✓ Streamlit version:', streamlit.__version__); print('✓ Librosa version:', librosa.__version__)"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo ✅ Setup complete! Starting the app...
    echo ================================================
    echo.
    streamlit run app.py
) else (
    echo.
    echo ❌ Installation verification failed!
    echo Please check the error messages above.
    pause
)
