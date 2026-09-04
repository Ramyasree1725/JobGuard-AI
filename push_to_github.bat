@echo off
echo =======================================================
echo      JobGuard AI - Automated GitHub Push Helper
echo =======================================================
echo.

cd /d "%~dp0"

echo [1/4] Adding all files to Git staging...
git add .

echo [2/4] Committing changes...
git commit -m "feat: complete full-stack JobGuard AI platform with frontend and backend"

echo [3/4] Ensuring main branch...
git branch -M main

echo.
git remote get-url origin >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Existing remote origin found. Pushing to GitHub...
    git push -u origin main
) else (
    echo.
    echo Please enter your GitHub Repository URL 
    echo (Example: https://github.com/YourUsername/jobguard-ai.git):
    set /p REPO_URL="Repository URL: "
    if not "%REPO_URL%"=="" (
        git remote add origin %REPO_URL%
        echo [4/4] Pushing code to GitHub...
        git push -u origin main
    ) else (
        echo No repository URL provided. Push cancelled.
    )
)

echo.
echo =======================================================
echo               Operation Completed!
echo =======================================================
pause
