@echo off
rem Agents Everywhere - Windows launcher. Double-click. No terminal typing.
rem 1) AitherZero bootstrap: PowerShell 7, toolchain, adk, awsh  (dev-workstation)
rem 2) connect: sign in (browser), inference, wire Claude Code to the MCP gateway
title Agents Everywhere - setting up this PC
echo.
echo   Agents Everywhere - one click, this PC becomes a connected agent node.
echo   Step 1/2  tools    (Python, Git, Node, gh, adk, awsh)
echo   Step 2/2  connect  (sign in - a browser tab will open - inference, IDE wiring)
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol='Tls12'; $env:AITHERZERO_PLAYBOOK='dev-workstation'; irm https://raw.githubusercontent.com/Aitherium/AitherZero/main/bootstrap.ps1 | iex"
if errorlevel 1 goto :fail
powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol='Tls12'; $env:AITHERZERO_PLAYBOOK='connect'; irm https://raw.githubusercontent.com/Aitherium/AitherZero/main/bootstrap.ps1 | iex"
if errorlevel 1 goto :fail
echo.
echo   DONE. Open a new terminal and type:  awsh
echo   (Claude Code / Cursor are already wired to the Aitherium MCP gateway.)
echo.
pause
exit /b 0
:fail
echo.
echo   Something failed above. Re-run this file - every step is idempotent and picks up where it left off.
echo.
pause
exit /b 1
