@echo off
call %~dp0env.bat
cd %WINPYDIR%\Scripts
%WINPYDIR%\python.exe -m spyderlib.start_app --light %*