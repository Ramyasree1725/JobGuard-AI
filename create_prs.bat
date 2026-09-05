@echo off
title JobGuard AI - PR Status and Creator
echo =======================================================
echo      JobGuard AI - Automatic GitHub PR Creator
echo =======================================================
echo.

cd /d "%~dp0"
python create_remaining_prs.py

echo.
pause
