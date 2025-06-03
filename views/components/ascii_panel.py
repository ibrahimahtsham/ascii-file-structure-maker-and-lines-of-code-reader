"""
ASCII tree display panel
"""
import tkinter as tk
from tkinter import ttk
from utils.theme import ModernTheme

class AsciiPanel:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.theme = ModernTheme()
        self.create_widgets()
    
    def create_widgets(self):
        """Create ASCII panel widgets"""
        # Main frame
        self.ascii_frame = tk.Frame(self.parent, bg=self.theme.BACKGROUND_SECONDARY)
        
        # Title
        self.ascii_label = tk.Label(
            self.ascii_frame,
            text="🌳 ASCII File Structure",
            **self.theme.get_label_style(12, "bold")
        )
        self.ascii_label.pack(pady=(0, 10))
        
        # Text area with scrollbar
        text_container = tk.Frame(self.ascii_frame, bg=self.theme.BACKGROUND_SECONDARY)
        text_container.pack(fill=tk.BOTH, expand=True)
        
        # Text widget
        self.ascii_tree_text = tk.Text(
            text_container,
            wrap=tk.NONE,
            bg=self.theme.BACKGROUND_PRIMARY,
            fg=self.theme.TEXT_PRIMARY,
            font=(self.theme.FONT_MONO, 10),
            insertbackground=self.theme.TEXT_PRIMARY,
            selectbackground=self.theme.ACCENT_BLUE,
            relief="flat",
            padx=10,
            pady=10
        )
        self.ascii_tree_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Vertical scrollbar
        self.text_scroll_v = ttk.Scrollbar(
            text_container,
            orient=tk.VERTICAL,
            command=self.ascii_tree_text.yview
        )
        self.text_scroll_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.ascii_tree_text.config(yscrollcommand=self.text_scroll_v.set)
        
        # Horizontal scrollbar
        self.text_scroll_h = ttk.Scrollbar(
            self.ascii_frame,
            orient=tk.HORIZONTAL,
            command=self.ascii_tree_text.xview
        )
        self.text_scroll_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.ascii_tree_text.config(xscrollcommand=self.text_scroll_h.set)
        
        # Configure text tags for syntax highlighting
        self.configure_text_tags()
    
    def configure_text_tags(self):
        """Configure text tags for different content types"""
        self.ascii_tree_text.tag_configure(
            "folder_total",
            foreground=self.theme.TEXT_ACCENT,
            font=(self.theme.FONT_MONO, 10, "bold")
        )
        self.ascii_tree_text.tag_configure(
            "file_lines",
            foreground=self.theme.TEXT_SUCCESS,
            font=(self.theme.FONT_MONO, 10)
        )
        self.ascii_tree_text.tag_configure(
            "grand_total",
            foreground=self.theme.ACCENT_RED,
            font=(self.theme.FONT_MONO, 12, "bold")
        )
        self.ascii_tree_text.tag_configure(
            "tree_structure",
            foreground=self.theme.TEXT_SECONDARY,
            font=(self.theme.FONT_MONO, 10)
        )
    
    def display_ascii_tree(self, folder_path, ignore_folders):
        """Display ASCII tree structure"""
        self.ascii_tree_text.delete(1.0, tk.END)
        
        if not folder_path:
            self.ascii_tree_text.insert(tk.END, "No folder selected")
            return
        
        # Generate tree
        ascii_tree, total_lines = self.controller.file_manager.generate_ascii_tree(
            folder_path, ignore_folders
        )
        
        # Insert tree content
        self.ascii_tree_text.insert(tk.END, ascii_tree)
        
        # Add summary
        summary = f"\n🎯 TOTAL LINES IN FOLDER: {total_lines:,}\n"
        summary += f"📁 Folder: {folder_path}"
        self.ascii_tree_text.insert(tk.END, summary)
        
        # Apply formatting
        self.apply_text_formatting()
    
    def apply_text_formatting(self):
        """Apply syntax highlighting to the text"""
        content = self.ascii_tree_text.get(1.0, tk.END)
        lines = content.split('\n')
        
        self.ascii_tree_text.delete(1.0, tk.END)
        
        for line in lines:
            if "total lines)" in line:
                self.ascii_tree_text.insert(tk.END, line + '\n', "folder_total")
            elif " lines)" in line and "total" not in line:
                self.ascii_tree_text.insert(tk.END, line + '\n', "file_lines")
            elif "TOTAL LINES IN FOLDER:" in line:
                self.ascii_tree_text.insert(tk.END, line + '\n', "grand_total")
            elif line.startswith(('├──', '└──', '│')):
                self.ascii_tree_text.insert(tk.END, line + '\n', "tree_structure")
            else:
                self.ascii_tree_text.insert(tk.END, line + '\n')
    
    def get_content(self):
        """Get the current ASCII tree content"""
        return self.ascii_tree_text.get(1.0, tk.END)
    
    def get_frame(self):
        """Get the main frame"""
        return self.ascii_frame