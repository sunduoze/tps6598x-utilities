@echo off
call %~dp0env.bat
echo patch pip and current launchers fopr move
rem %WINPYDIR%\python.exe -c "from winpython.utils import patch_sourcefile;patch_sourcefile(r'%WINPYDIR%\Lib\site-packages\pip\_vendor\distlib\scripts.py', 'executable = get_executable()', 'executable = os.path.join(os.path.basename(get_executable()))' )"

%WINPYDIR%\python.exe -c "from winpython import wppm;dist=wppm.Distribution(r'%WINPYDIR%');dist.patch_standard_packages('pip');dist.patch_all_shebang(to_movable=True)"
pause
        