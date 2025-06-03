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
echo 4. Build EXE (safer method)
echo 5. Run built EXE
echo 6. Clean build files
echo 7. Run tests
echo 8. Check imports
echo 9. Add Defender exclusions (manual)
echo 10. Exit
echo.
set /p choice="Enter your choice (1-10): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto run
if "%choice%"=="3" goto build
if "%choice%"=="4" goto build_safe
if "%choice%"=="5" goto run_exe
if "%choice%"=="6" goto clean
if "%choice%"=="7" goto test
if "%choice%"=="8" goto check_imports
if "%choice%"=="9" goto defender_exclusions
if "%choice%"=="10" goto exit

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
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"
echo Building executable...
pyinstaller --onefile --windowed --name "FileStructureViewer_v3" --version-file=version_info.txt main.py
if exist "dist\FileStructureViewer_v3.exe" (
    echo ✅ Build successful! EXE created at: dist\FileStructureViewer_v3.exe
) else (
    echo ❌ Build failed! Check for errors above.
)
pause
goto menu

:build_safe
echo Building with safer options...
echo Step 1: Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"
echo Step 2: Create spec file
pyi-makespec --onefile --windowed --name "FileStructureViewer_v3" main.py
echo Step 3: Build with spec
pyinstaller FileStructureViewer_v3.spec
if exist "dist\FileStructureViewer_v3.exe" (
    echo ✅ Build successful! EXE created at: dist\FileStructureViewer_v3.exe
) else (
    echo ❌ Build failed! Check for errors above.
)
pause
goto menu

:run_exe
echo Running built EXE...
if exist "dist\FileStructureViewer_v3.exe" (
    echo Starting FileStructureViewer_v3.exe...
    start "" "dist\FileStructureViewer_v3.exe"
    echo Application started!
) else (
    echo EXE not found! Please build first (option 3 or 4).
    echo Looking for: %cd%\dist\FileStructureViewer_v3.exe
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

:defender_exclusions
echo Adding Defender exclusions (manual)...
echo Please follow these steps:
echo 1. Open Windows Security.
echo 2. Go to "Virus & threat protection".
echo 3. Click on "Manage settings" under "Virus & threat protection settings".
echo 4. Scroll down to "Exclusions" and click on "Add or remove exclusions".
echo 5. Add the following paths as exclusions:
echo    - %cd%\dist\FileStructureViewer_v3.exe
echo    - %cd%\build
echo    - %cd%\__pycache__
echo    - %cd%\models\__pycache__
echo    - %cd%\views\__pycache__
echo    - %cd%\controllers\__pycache__
echo    - %cd%\utils\__pycache__
echo 6. Close Windows Security.
echo.
echo Note: These steps are for manual exclusion. Automating this process is not recommended due to security risks.
pause
goto menu

:exit
echo Goodbye!
pause
exit