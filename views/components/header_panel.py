"""
Header panel with folder selection and action buttons
"""
import tkinter as tk
from tkinter import filedialog
from utils.theme import ModernTheme
from utils.constants import DEFAULT_IGNORE_FOLDERS

class HeaderPanel:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.theme = ModernTheme()
        
        # Variables
        self.folder_var = tk.StringVar()
        self.ignore_var = tk.StringVar()
        self.ignore_var.set(DEFAULT_IGNORE_FOLDERS)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create header panel widgets"""
        # Main header frame
        self.header_frame = tk.Frame(
            self.parent, 
            bg=self.theme.BACKGROUND_SECONDARY, 
            pady=15
        )
        self.header_frame.pack(fill=tk.X, padx=15, pady=(10, 0))
        
        # Folder selection section
        self.create_folder_section()
        
        # Ignore folders section
        self.create_ignore_section()
        
        # Action buttons section
        self.create_actions_section()
    
    def create_folder_section(self):
        """Create folder selection row"""
        folder_row = tk.Frame(self.header_frame, bg=self.theme.BACKGROUND_SECONDARY)
        folder_row.pack(fill=tk.X, pady=(0, 10))
        
        # Folder label
        folder_label = tk.Label(
            folder_row,
            text="📂 Select Folder:",
            **self.theme.get_label_style(11, "bold")
        )
        folder_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Folder entry
        self.folder_entry = tk.Entry(
            folder_row,
            textvariable=self.folder_var,
            **self.theme.get_entry_style()
        )
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        # Browse button
        self.browse_button = tk.Button(
            folder_row,
            text="🔍 Browse",
            command=self.browse_folder,
            **self.theme.get_button_style(self.theme.ACCENT_BLUE, self.theme.ACCENT_BLUE_HOVER)
        )
        self.browse_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh button
        self.refresh_button = tk.Button(
            folder_row,
            text="🔄 Refresh",
            command=self.refresh_display,
            **self.theme.get_button_style(self.theme.ACCENT_ORANGE)
        )
        self.refresh_button.pack(side=tk.LEFT)
    
    def create_ignore_section(self):
        """Create ignore folders section"""
        ignore_row = tk.Frame(self.header_frame, bg=self.theme.BACKGROUND_SECONDARY)
        ignore_row.pack(fill=tk.X, pady=(0, 10))
        
        # Ignore label
        ignore_label = tk.Label(
            ignore_row,
            text="🚫 Ignore Folders:",
            **self.theme.get_label_style(10, "bold")
        )
        ignore_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Ignore entry
        self.ignore_entry = tk.Entry(
            ignore_row,
            textvariable=self.ignore_var,
            **self.theme.get_entry_style()
        )
        self.ignore_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def create_actions_section(self):
        """Create action buttons section"""
        actions_row = tk.Frame(self.header_frame, bg=self.theme.BACKGROUND_SECONDARY)
        actions_row.pack(fill=tk.X)
        
        # Copy all files button
        self.copy_all_button = tk.Button(
            actions_row,
            text="📄 Copy All Files",
            command=self.copy_all_files,
            **self.theme.get_button_style(self.theme.ACCENT_GREEN)
        )
        self.copy_all_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Copy ASCII tree button
        self.copy_tree_button = tk.Button(
            actions_row,
            text="🌳 Copy ASCII Tree",
            command=self.copy_ascii_tree,
            **self.theme.get_button_style(self.theme.ACCENT_PURPLE)
        )
        self.copy_tree_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Statistics button
        self.stats_button = tk.Button(
            actions_row,
            text="📊 Show Stats",
            command=self.show_statistics,
            **self.theme.get_button_style(self.theme.BACKGROUND_TERTIARY)
        )
        self.stats_button.pack(side=tk.LEFT)
    
    def browse_folder(self):
        """Handle folder browsing"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_var.set(folder_path)
            self.controller.load_folder(folder_path)
    
    def refresh_display(self):
        """Handle refresh button click"""
        self.controller.refresh_display()
    
    def copy_all_files(self):
        """Handle copy all files button click"""
        self.controller.copy_all_files()
    
    def copy_ascii_tree(self):
        """Handle copy ASCII tree button click"""
        self.controller.copy_ascii_tree()
    
    def show_statistics(self):
        """Handle show statistics button click"""
        self.controller.show_statistics()
    
    def get_folder_path(self):
        """Get current folder path"""
        return self.folder_var.get()
    
    def get_ignore_folders(self):
        """Get list of ignored folders"""
        return [f.strip() for f in self.ignore_var.get().split(",") if f.strip()]