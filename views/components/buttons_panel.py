"""
Individual file copy buttons panel
"""
import tkinter as tk
from tkinter import ttk
import os
from utils.theme import ModernTheme

class ButtonsPanel:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.theme = ModernTheme()
        self.buttons = []
        self.create_widgets()
    
    def create_widgets(self):
        """Create buttons panel widgets"""
        # Main frame
        self.buttons_frame = tk.Frame(self.parent, bg=self.theme.BACKGROUND_SECONDARY)
        
        # Title
        self.buttons_label = tk.Label(
            self.buttons_frame,
            text="📋 Copy Individual Files",
            **self.theme.get_label_style(12, "bold")
        )
        self.buttons_label.pack(pady=(0, 10))
        
        # Scrollable area
        self.create_scrollable_area()
    
    def create_scrollable_area(self):
        """Create scrollable area for buttons"""
        # Canvas and scrollbar
        self.buttons_canvas = tk.Canvas(
            self.buttons_frame,
            bg=self.theme.BACKGROUND_SECONDARY,
            highlightthickness=0
        )
        self.buttons_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.buttons_scroll = ttk.Scrollbar(
            self.buttons_frame,
            orient=tk.VERTICAL,
            command=self.buttons_canvas.yview
        )
        self.buttons_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Inner frame for buttons
        self.buttons_inner_frame = tk.Frame(
            self.buttons_canvas,
            bg=self.theme.BACKGROUND_SECONDARY
        )
        
        self.buttons_canvas.create_window(
            (0, 0),
            window=self.buttons_inner_frame,
            anchor=tk.NW
        )
        
        # Configure scrolling
        self.buttons_inner_frame.bind(
            "<Configure>",
            lambda e: self.buttons_canvas.configure(scrollregion=self.buttons_canvas.bbox("all"))
        )
        self.buttons_canvas.configure(yscrollcommand=self.buttons_scroll.set)
        
        # Mouse wheel binding
        self.buttons_canvas.bind("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.buttons_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def clear_buttons(self):
        """Clear all file copy buttons"""
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
    
    def populate_buttons(self, folder_path, ignore_folders):
        """Create copy buttons for all files in folder"""
        self.clear_buttons()
        
        if not os.path.exists(folder_path):
            return
        
        file_count = 0
        for root, dirs, files in os.walk(folder_path):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_folders]
            
            for file in files:
                file_path = os.path.join(root, file)
                lines = self.controller.file_manager.count_lines_of_code(file_path)
                
                if lines > 0:
                    self.create_file_button(file_path, file, lines)
                    file_count += 1
        
        # Update scroll region
        self.buttons_inner_frame.update_idletasks()
        self.buttons_canvas.configure(scrollregion=self.buttons_canvas.bbox("all"))
    
    def create_file_button(self, file_path, file_name, lines):
        """Create a button for copying individual file"""
        # Determine file type for icon
        ext = os.path.splitext(file_name)[1].lower()
        icon = self.get_file_icon(ext)
        
        button_text = f"{icon} {file_name} ({lines} lines)"
        
        copy_button = tk.Button(
            self.buttons_inner_frame,
            text=button_text,
            command=lambda: self.controller.copy_single_file(file_path),
            bg=self.theme.ACCENT_BLUE,
            fg=self.theme.TEXT_PRIMARY,
            activebackground=self.theme.ACCENT_BLUE_HOVER,
            activeforeground=self.theme.TEXT_PRIMARY,
            font=(self.theme.FONT_FAMILY, 9),
            relief="flat",
            cursor="hand2",
            anchor="w",
            padx=15,
            pady=8
        )
        copy_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=3)
        
        # Add hover effect
        copy_button.bind("<Enter>", lambda e: copy_button.config(bg=self.theme.ACCENT_BLUE_HOVER))
        copy_button.bind("<Leave>", lambda e: copy_button.config(bg=self.theme.ACCENT_BLUE))
        
        self.buttons.append(copy_button)
    
    def get_file_icon(self, extension):
        """Get appropriate icon for file type"""
        icons = {
            '.py': '🐍', '.js': '📜', '.ts': '📘', '.html': '🌐', '.css': '🎨',
            '.java': '☕', '.cpp': '⚙️', '.c': '⚙️', '.h': '📋', '.cs': '🔷',
            '.php': '🌐', '.rb': '💎', '.go': '🐹', '.rs': '🦀', '.swift': '🍎',
            '.kt': '🤖', '.dart': '🎯', '.vue': '💚', '.jsx': '⚛️', '.tsx': '⚛️',
            '.json': '📋', '.xml': '📄', '.md': '📝', '.txt': '📄', '.yml': '⚙️',
            '.yaml': '⚙️', '.sql': '🗃️', '.sh': '🐚', '.bat': '🖥️', '.ps1': '💙'
        }
        return icons.get(extension, '📄')
    
    def get_frame(self):
        """Get the main frame"""
        return self.buttons_frame