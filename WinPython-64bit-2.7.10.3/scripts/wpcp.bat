@echo off
call %~dp0env.bat
cd %WINPYDIR%\Scripts
%WINPYDIR%\python.exe -m winpython.controlpanel %*