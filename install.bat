@echo off
echo Installing PortScan Pro...
echo.

REM Install dependencies
echo Installing Python packages...
python -m pip install --upgrade pip
pip install customtkinter==5.2.1
pip install pillow==10.1.0
pip install reportlab==4.0.7
pip install pandas==2.1.4

echo.
echo ✅ Installation complete!
echo.
echo To run the application:
echo python main.py
echo.
pause