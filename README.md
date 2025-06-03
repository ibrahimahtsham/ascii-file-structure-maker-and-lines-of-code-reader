# File Structure Viewer - ASCII Tree Generator & Code Copier

A modern Python GUI application that helps developers easily copy entire codebases with file structures to share with AI assistants like ChatGPT. Perfect for getting code reviews, debugging help, or architectural advice.

## ✨ Features

- 📁 **Browse & Analyze** - Select any folder and instantly see its structure
- 🌳 **ASCII Tree Generation** - Beautiful tree visualization of your project structure
- 📄 **Smart File Copying** - Copy individual files or entire codebases with proper formatting
- 📊 **Project Statistics** - View file counts, lines of code, and file type distributions
- 🎨 **Modern Dark Theme** - Clean, professional interface that's easy on the eyes
- ⚡ **Fast & Lightweight** - Built with Python Tkinter for optimal performance
- 🔍 **Folder Filtering** - Ignore common folders like `node_modules`, `.git`, `__pycache__`

## 🖼️ Version Comparison

### Previous Version (v2)

![Old Version](https://github.com/ibrahimahtsham/ascii-file-structure-maker-and-lines-of-code-reader/assets/111352185/f9ef5de9-5f05-4b9e-8894-1bb797c91523)

### Current Version (v3) - Modern UI

_[Add your new screenshot here showing the modern dark theme interface with the improved layout]_

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation & Usage

1. **Clone the repository**

   ```bash
   git clone https://github.com/ibrahimahtsham/ascii-file-structure-maker-and-lines-of-code-reader.git
   cd ascii-file-structure-maker-and-lines-of-code-reader
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   # or manually:
   pip install pyperclip cx_Freeze
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### Building Executable

**Windows:**

```bash
run_project.bat
```

**Linux:**

```bash
chmod +x build_linux.sh
./build_linux.sh
```

## 💡 Use Cases

- **AI-Assisted Development** - Share your entire codebase structure with ChatGPT, Claude, or other AI assistants
- **Code Reviews** - Quickly share project structure and specific files with team members
- **Documentation** - Generate ASCII tree representations for README files or documentation
- **Project Analysis** - Get insights into your project's file distribution and size
- **Learning** - Understand the structure of open-source projects

## 🛠️ Technical Stack

- **GUI Framework**: Python Tkinter with custom modern theme
- **File Operations**: Native Python `os` and `pathlib` modules
- **Clipboard Integration**: `pyperclip` for seamless copy operations
- **Build System**: `cx_Freeze` for cross-platform executable generation

## 📋 Project Structure

```
ascii-file-structure-maker-and-lines-of-code-reader/
├── main.py                 # Application entry point
├── controllers/            # Business logic
│   └── main_controller.py
├── models/                 # Data management
│   └── file_manager.py
├── views/                  # UI components
│   ├── main_window.py
│   └── components/
│       └── header_panel.py
├── utils/                  # Utilities
│   ├── theme.py           # Modern dark theme
│   └── constants.py
└── build/                 # Generated executables
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs or suggest features via Issues
- Submit Pull Requests with improvements
- Share feedback on the user experience

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
