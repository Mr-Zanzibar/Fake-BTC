@echo off

echo  Select an option:
echo  1. Run the Python code
echo  2. Compile the Python code into an .exe file
echo  3. Display the credits list

set /p choice=Enter the option number:

if "%choice%"=="1" (
    pip install ecdsa base58
    python miner.py
) else if "%choice%"=="2" (
    pip install pyinstaller
    pyinstaller --onefile miner.py
    rmdir /s /q build
    del /s /q miner.py.spec
    echo The .exe file has been created successfully.
) else if "%choice%"=="3" (
    echo Credits:
    echo - Mr-Zanzibar: https://github.com/Mr-Zanzibar/Fake-BTC
    echo - Discord: don.zanzibar
) else (
    echo Invalid option.
)

pause

