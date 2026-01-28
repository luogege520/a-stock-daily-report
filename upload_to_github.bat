@echo off
chcp 65001 >nul
echo ====================================================
echo Upload to GitHub - AkShare Version
echo ====================================================
echo.

echo Please enter your GitHub repository URL:
echo Example: https://github.com/username/a-stock-daily-report.git
set /p REPO_URL=Repository URL: 

echo.
echo [1/5] Cloning repository...
cd /d D:\阶跃AI
if exist temp-upload rmdir /S /Q temp-upload
git clone %REPO_URL% temp-upload
if errorlevel 1 (
    echo Error: Failed to clone repository
    pause
    exit /b 1
)
cd temp-upload

echo.
echo [2/5] Copying new files...
copy "..\a-stock-daily-report\fetch_data.py" . /Y
copy "..\a-stock-daily-report\generate_report.py" . /Y
copy "..\a-stock-daily-report\main.py" . /Y
copy "..\a-stock-daily-report\requirements.txt" . /Y
if exist "..\a-stock-daily-report\send_email.py" copy "..\a-stock-daily-report\send_email.py" . /Y

echo.
echo [3/5] Viewing changes...
git status

echo.
echo [4/5] Committing changes...
git add .
git commit -m "Update to v2.0.0: Use AkShare for real market data"

echo.
echo [5/5] Pushing to GitHub...
git push

if errorlevel 1 (
    echo.
    echo Error: Push failed. You may need to enter credentials.
    echo Please try again or use GitHub Desktop.
    pause
    cd ..
    exit /b 1
)

echo.
echo ====================================================
echo Upload completed successfully!
echo ====================================================
echo.
echo Next steps:
echo 1. Visit your GitHub repository to verify files
echo 2. Go to Actions page to test run
echo 3. Check your email for the report
echo.

cd ..
rmdir /S /Q temp-upload

pause
