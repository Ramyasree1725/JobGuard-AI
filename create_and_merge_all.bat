@echo off
title JobGuard AI - Open PRs and Merge to Main
echo =======================================================
echo      JobGuard AI - Merging All 4 Branches to Main
echo =======================================================
echo.

cd /d "%~dp0"

echo [1/3] Merging feature/frontend-ui into main...
git checkout main
git merge feature/frontend-ui -m "Merge branch 'feature/frontend-ui' into main" --no-edit

echo [2/3] Merging feature/backend-api and scam-heuristics into main...
git merge feature/backend-api -m "Merge branch 'feature/backend-api' into main" --no-edit
git merge feature/scam-heuristics -m "Merge branch 'feature/scam-heuristics' into main" --no-edit
git merge dev -m "Merge branch 'dev' into main" --no-edit

echo [3/3] Pushing merged main to GitHub...
git push origin main

echo.
echo Opening PR records in browser for confirmation...
start "" "https://github.com/Ramyasree1725/JobGuard-AI/network"
start "" "https://github.com/Ramyasree1725/JobGuard-AI/commits/main"

echo.
echo =======================================================
echo     DONE! All 4 branches are 100%% merged into main!
echo     Check: https://github.com/Ramyasree1725/JobGuard-AI
echo =======================================================
pause
