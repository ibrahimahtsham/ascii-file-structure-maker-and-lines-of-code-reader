#!/bin/bash
# filepath: build_linux.sh

echo "==========================================="
echo "File Structure Viewer - Linux Builder"
echo "==========================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "Installing dependencies..."
pip3 install pyperclip cx_Freeze

echo "Building Linux binary..."
python3 setup.py build

echo "✅ Linux build complete!"
echo "Binary location: build/exe.linux-x86_64-*/FileStructureViewer_v3_Linux"

# Make the built file executable
find build -name "FileStructureViewer_v3_Linux" -exec chmod +x {} \;

echo "✅ Binary is now executable!"