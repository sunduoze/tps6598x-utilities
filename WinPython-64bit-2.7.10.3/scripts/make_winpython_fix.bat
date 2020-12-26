@echo off
call %~dp0env.bat
echo patch pip and current launchers for non-move
%WINPYDIR%\python.exe -c "from winpython.utils import patch_sourcefile;patch_sourcefile(r'%WINPYDIR%\Lib\site-packages\pip\_vendor\distlib\scripts.py', 'executable = os.path.join(os.path.basename(get_executable()))', 'executable = get_executable()' )"

%WINPYDIR%\python.exe -c "from winpython import wppm;dist=wppm.Distribution(r'%WINPYDIR%');dist.patch_all_shebang(to_movable=False)"
pause
        