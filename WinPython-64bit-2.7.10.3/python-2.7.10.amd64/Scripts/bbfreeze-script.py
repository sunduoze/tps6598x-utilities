#!C:\Python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'bbfreeze==1.1.3','console_scripts','bbfreeze'
__requires__ = 'bbfreeze==1.1.3'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('bbfreeze==1.1.3', 'console_scripts', 'bbfreeze')()
    )
