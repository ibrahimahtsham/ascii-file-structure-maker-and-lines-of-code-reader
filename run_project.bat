@echo off
echo ==========================================
echo File Structure Viewer v3.0 - Project Manager  
echo ==========================================
echo.

:menu
echo Select an option:
echo 1. Install dependencies
echo 2. Run project (development)
echo 3. Build EXE (GUI only, no console)
echo 4. Run built EXE
echo 5. Clean build files
echo 6. Run tests
echo 7. Check imports
echo 8. Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto run
if "%choice%"=="3" goto build
if "%choice%"=="4" goto run_exe
if "%choice%"=="5" goto clean
if "%choice%"=="6" goto test
if "%choice%"=="7" goto check_imports
if "%choice%"=="8" goto exit

echo Invalid choice. Please try again.
echo.
goto menu

:install
echo Installing dependencies...
pip install pyperclip pyinstaller
echo Dependencies installed!
echo.
pause
goto menu

:run
echo ==========================================
echo Running project in development mode...
echo Press Ctrl+C to stop the application
echo ==========================================
python main.py
echo.
echo Application closed.
pause
goto menu

:build
echo Building EXE (GUI only, no console window)...
pyinstaller --onefile --windowed --name "FileStructureViewer_v3" main.py
echo Build complete! EXE created in dist folder.
echo.
pause
goto menu

:run_exe
echo Running built EXE...
if exist "dist\FileStructureViewer_v3.exe" (
    "dist\FileStructureViewer_v3.exe"
) else (
    echo EXE not found! Please build first (option 3).
)
pause
goto menu

:test
echo Running basic tests...
echo Testing imports...
python -c "import sys; print('Python version:', sys.version)"
python -c "from models.file_manager import FileManager; print('✅ FileManager imported successfully')"
python -c "from controllers.main_controller import MainController; print('✅ Controller imported successfully')" 
python -c "from views.main_window import MainWindow; print('✅ MainWindow imported successfully')"
python -c "from utils.theme import ModernTheme; print('✅ Theme imported successfully')"
python -c "from utils.constants import WINDOW_TITLE; print('✅ Constants imported successfully')"
echo Tests completed!
pause
goto menu

:check_imports
echo Checking all imports...
python -c "
try:
    import tkinter as tk
    print('✅ tkinter imported')
    import pyperclip
    print('✅ pyperclip imported')
    from models.file_manager import FileManager
    print('✅ FileManager imported')
    from views.main_window import MainWindow  
    print('✅ MainWindow imported')
    from controllers.main_controller import MainController
    print('✅ MainController imported')
    from utils.theme import ModernTheme
    print('✅ ModernTheme imported')
    from utils.constants import WINDOW_TITLE
    print('✅ Constants imported')
    print('🎉 All imports successful!')
except Exception as e:
    print('❌ Import error:', str(e))
    import traceback
    traceback.print_exc()
"
pause
goto menu

:clean
echo Cleaning build files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "models\__pycache__" rmdir /s /q "models\__pycache__"
if exist "views\__pycache__" rmdir /s /q "views\__pycache__"
if exist "controllers\__pycache__" rmdir /s /q "controllers\__pycache__"
if exist "utils\__pycache__" rmdir /s /q "utils\__pycache__"
if exist "views\components\__pycache__" rmdir /s /q "views\components\__pycache__"
echo Build files cleaned!
echo.
pause
goto menu

:exit
echo Goodbye!
pause
exit