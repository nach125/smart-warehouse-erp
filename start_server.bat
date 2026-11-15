@echo off
title Smart Warehouse ERP - Localhost Server
echo ============================================================
echo Starting Smart Warehouse ERP Web Server on http://localhost:8080/
echo ============================================================
powershell -ExecutionPolicy Bypass -File "%~dp0server.ps1"
pause
