@echo off
rem Agents Everywhere - Windows launcher. Double-click. No terminal typing.
rem Runs the AitherZero playbooks dev-workstation (tools) then connect (sign in, inference, IDE wiring).
title Agents Everywhere - setting up this PC
echo.
echo   Agents Everywhere - one click, this PC becomes a connected agent node.
echo   Step 1/2  tools    (Python, Git, Node, gh, adk, awsh)
echo   Step 2/2  connect  (sign in - a browser tab will open - inference, IDE wiring)
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "='dev-workstation,connect'; irm https://raw.githubusercontent.com/Aitherium/AitherZero/main/bootstrap.ps1 | iex"
echo.
echo   Finished. Open a NEW terminal and type:  awsh
echo   If anything failed above, run this file again - every step is idempotent.
echo.
pause