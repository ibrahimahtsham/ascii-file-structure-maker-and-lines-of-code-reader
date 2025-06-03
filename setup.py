from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {
    'packages': ['tkinter', 'os', 'pyperclip'],
    'excludes': [],
    'include_files': []
}

base = None
if sys.platform == "win32":
    base = 'Win32GUI'  # Use this for Windows GUI applications

executables = [
    Executable('main.py', 
              base=base, 
              target_name='FileStructureViewer_v3_Linux')
]

setup(
    name='FileStructureViewer',
    version='3.0',
    description='Modern file structure viewer and analyzer',
    options={'build_exe': build_options},
    executables=executables
)