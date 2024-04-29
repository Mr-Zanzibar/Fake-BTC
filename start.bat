@echo off

echo Select an option:
echo 1. Run the Python code
echo 2. Compile the Python code into an .exe file
echo 3. Display the credits list

:option
set /p choice=Enter the option number: 

if "%choice%"=="1" (
    pip install ecdsa base58
    python miner.py
) else if "%choice%"=="2" (
    pip install pyinstaller
    pyinstaller --onefile miner.py
    rmdir /s /q build
    del /s /q miner.py.spec
    cls
    powershell -Command Write-Host "The .exe file has been created successfully." -ForegroundColor Green
    pause
) else if "%choice%"=="3" (
    echo Mr-Zanzibar
    start https://github.com/Mr-Zanzibar/Fake-BTC
    timeout /t 5 /nobreak >nul
    goto :option
) else (
    powershell -Command Write-Host "Invalid option." -ForegroundColor Red
    timeout /t 2 /nobreak >nul
    goto :option
)
