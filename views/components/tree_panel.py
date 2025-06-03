"""
Tree view panel for displaying file structure
"""
import tkinter as tk
from tkinter import ttk
import os
from utils.theme import ModernTheme

class TreePanel:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.theme = ModernTheme()
        self.create_widgets()
    
    def create_widgets(self):
        """Create tree panel widgets"""
        # Main frame
        self.tree_frame = tk.Frame(self.parent, bg=self.theme.BACKGROUND_SECONDARY)
        
        # Title
        self.tree_label = tk.Label(
            self.tree_frame,
            text="📁 File Structure",
            **self.theme.get_label_style(12, "bold")
        )
        self.tree_label.pack(pady=(0, 10))
        
        # Tree frame with scrollbar
        tree_container = tk.Frame(self.tree_frame, bg=self.theme.BACKGROUND_SECONDARY)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        self.tree_scroll = ttk.Scrollbar(tree_container)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.file_tree = ttk.Treeview(
            tree_container,
            yscrollcommand=self.tree_scroll.set,
            show='tree'
        )
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.file_tree.yview)
        
        # Configure tree tags
        self.file_tree.tag_configure("folder", foreground=self.theme.TREE_FOLDER)
        self.file_tree.tag_configure("file", foreground=self.theme.TREE_FILE)
        self.file_tree.tag_configure("error", foreground=self.theme.TREE_ERROR)
        
        # Bind events
        self.file_tree.bind('<Double-1>', self.on_double_click)
    
    def clear_tree(self):
        """Clear the tree view"""
        self.file_tree.delete(*self.file_tree.get_children())
    
    def populate_tree(self, folder_path, ignore_folders):
        """Populate tree with folder structure"""
        self.clear_tree()
        
        if not os.path.exists(folder_path):
            self.file_tree.insert("", "end", text="Invalid folder path", tags=("error",))
            return
        
        root_node = self.file_tree.insert(
            "", "end", 
            text=f"📁 {os.path.basename(folder_path)}", 
            open=True,
            tags=("folder",)
        )
        
        self._populate_node(folder_path, root_node, ignore_folders)
    
    def _populate_node(self, folder_path, parent_node, ignore_folders):
        """Recursively populate tree nodes"""
        try:
            items = os.listdir(folder_path)
        except PermissionError:
            self.file_tree.insert(parent_node, "end", text="Permission denied", tags=("error",))
            return
        
        # Sort items: folders first, then files
        items.sort(key=lambda x: (os.path.isfile(os.path.join(folder_path, x)), x.lower()))
        
        for item in items:
            if item in ignore_folders:
                continue
            
            item_path = os.path.join(folder_path, item)
            
            if os.path.isdir(item_path):
                node = self.file_tree.insert(
                    parent_node, "end",
                    text=f"📁 {item}",
                    open=False,
                    tags=("folder",),
                    values=(item_path,)
                )
                self._populate_node(item_path, node, ignore_folders)
            else:
                lines = self.controller.file_manager.count_lines_of_code(item_path)
                self.file_tree.insert(
                    parent_node, "end",
                    text=f"📄 {item} ({lines} lines)",
                    tags=("file",),
                    values=(item_path,)
                )
    
    def on_double_click(self, event):
        """Handle double-click on tree item"""
        if not self.file_tree.selection():
            return
        
        item = self.file_tree.selection()[0]
        values = self.file_tree.item(item, "values")
        
        if values and len(values) > 0:
            file_path = values[0]
            # Check if it's a file
            if os.path.isfile(file_path):
                self.controller.copy_single_file(file_path)
    
    def get_frame(self):
        """Get the main frame"""
        return self.tree_frame