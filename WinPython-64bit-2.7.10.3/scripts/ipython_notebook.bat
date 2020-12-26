@echo off
call %~dp0env.bat
cd %WINPYDIR%\Scripts
%WINPYDIR%\scripts\jupyter-notebook.exe --notebook-dir=%WINPYDIR%\..\notebooks %*
