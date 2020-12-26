@echo off
call %~dp0env.bat
cd %WINPYDIR%\Lib\site-packages\PyQt5\examples\qtdemo
%WINPYDIR%\python.exe qtdemo.py %*