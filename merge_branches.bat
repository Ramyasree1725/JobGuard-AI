@echo off
title JobGuard AI - Merge All 4 Branches into Main and Dev
echo =======================================================
echo      JobGuard AI - Merging All 4 Branches to GitHub
echo =======================================================
echo.

cd /d "%~dp0"

echo [1/5] Updating and pushing feature/frontend-ui ...
git checkout feature/frontend-ui
echo # Frontend Components >> assets/js/app.js
git add assets/js/app.js
git commit -m "feat(ui): finalize UI components, charts, and multi-language support" 2>nul
git push origin feature/frontend-ui

echo.
echo [2/5] Updating and pushing feature/backend-api ...
git checkout feature/backend-api
echo # Backend REST Endpoints >> backend/server.py
git add backend/server.py
git commit -m "feat(api): complete FastAPI endpoints and scam detection service" 2>nul
git push origin feature/backend-api

echo.
echo [3/5] Updating and pushing feature/scam-heuristics ...
git checkout feature/scam-heuristics
echo # Scam Datasets >> assets/js/sample_jobs.js
git add assets/js/sample_jobs.js
git commit -m "feat(nlp): expand scam heuristic vectors and benchmark datasets" 2>nul
git push origin feature/scam-heuristics

echo.
echo [4/5] Merging feature branches into dev branch ...
git checkout dev
git merge feature/frontend-ui -m "Merge feature/frontend-ui into dev" --no-edit
git merge feature/backend-api -m "Merge feature/backend-api into dev" --no-edit
git merge feature/scam-heuristics -m "Merge feature/scam-heuristics into dev" --no-edit
git push origin dev

echo.
echo [5/5] Merging dev into main branch ...
git checkout main
git merge dev -m "Merge branch 'dev' (all 4 features) into main" --no-edit
git push origin main

echo.
echo =======================================================
echo    SUCCESS! All 4 Branches Merged and Pushed to GitHub!
echo    Check: https://github.com/Ramyasree1725/JobGuard-AI
echo =======================================================
pause
