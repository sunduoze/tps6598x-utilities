@echo off
call %~dp0env.bat
cd %WINPYDIR%\Lib\site-packages\PyQt4\examples\demos\qtdemo
start %WINPYDIR%\pythonw.exe qtdemo.pyw %*