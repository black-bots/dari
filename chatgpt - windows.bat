@echo off
echo Opening BlackGPT...

REM Open powershell via bat
start powershell.exe -NoExit -Command "python path\to\BlackGPT.py"

REM The web page can be accessed with delayed start http://127.0.0.1:7860/
ping -n 5 127.0.0.1>nul

REM access chargpt via your browser (default microsoft edge browser)
start chrome:http://127.0.0.1:7860/


echo Finished opening BlackGPT (http://127.0.0.1:7860/).