@echo off
title JobGuard AI - GitHub Push
echo =======================================================
echo      JobGuard AI - Pushing to GitHub (Ramyasree1725)
echo =======================================================
echo.

cd /d "%~dp0"

echo [1/4] Staging all files...
git add .

echo.
echo [2/4] Committing code...
git commit -m "feat: complete full-stack JobGuard AI platform with frontend & backend"

echo.
echo [3/4] Setting main branch and origin URL...
git branch -M main
git remote set-url origin https://github.com/Ramyasree1725/JobGuard-AI.git 2>nul || git remote add origin https://github.com/Ramyasree1725/JobGuard-AI.git

echo.
echo [4/4] Pushing to https://github.com/Ramyasree1725/JobGuard-AI.git...
git push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [Retrying with Force Push in case GitHub repository has an existing README]...
    git push -u origin main --force
)

echo.
echo =======================================================
echo     Done! Check: https://github.com/Ramyasree1725/JobGuard-AI
echo =======================================================
pause

