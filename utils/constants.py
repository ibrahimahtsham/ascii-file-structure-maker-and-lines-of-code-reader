"""
Application constants and configuration
"""

# Window settings
WINDOW_TITLE = "📁 File Structure Viewer v3.0"
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800

# Default ignore folders
DEFAULT_IGNORE_FOLDERS = ".git,.gitignore,.expo,node_modules,.idea,__pycache__,dist,build,.pytest_cache,.vscode"

# File types for syntax highlighting
PROGRAMMING_EXTENSIONS = {
    '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.cs', '.php', 
    '.rb', '.go', '.rs', '.swift', '.kt', '.dart', '.vue', '.jsx', '.tsx'
}

# Status messages
STATUS_READY = "Ready"
STATUS_LOADING = "Loading..."
STATUS_REFRESHING = "Refreshing..."
STATUS_COPYING = "Copying files..."