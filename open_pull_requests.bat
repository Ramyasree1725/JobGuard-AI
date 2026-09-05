@echo off
title JobGuard AI - Open 4 Pull Requests in Browser
echo =======================================================
echo    Opening 4 Pull Request Pages in your Browser...
echo =======================================================
echo.

echo Opening PR 1: feature/frontend-ui -> main ...
start "" "https://github.com/Ramyasree1725/JobGuard-AI/compare/main...feature/frontend-ui?expand=1"

timeout /t 1 /nobreak >nul

echo Opening PR 2: feature/backend-api -> main ...
start "" "https://github.com/Ramyasree1725/JobGuard-AI/compare/main...feature/backend-api?expand=1"

timeout /t 1 /nobreak >nul

echo Opening PR 3: feature/scam-heuristics -> main ...
start "" "https://github.com/Ramyasree1725/JobGuard-AI/compare/main...feature/scam-heuristics?expand=1"

timeout /t 1 /nobreak >nul

echo Opening PR 4: dev -> main ...
start "" "https://github.com/Ramyasree1725/JobGuard-AI/compare/main...dev?expand=1"

echo.
echo =======================================================
echo  Browser tabs opened! Just click 'Create pull request'!
echo =======================================================
pause
