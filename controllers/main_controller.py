"""
Main application controller
"""
import os
import pyperclip
from models.file_manager import FileManager
from views.main_window import MainWindow
from utils.theme import ModernTheme
from utils.constants import STATUS_READY, STATUS_LOADING, STATUS_REFRESHING, STATUS_COPYING

class MainController:
    def __init__(self, root):
        self.root = root
        self.file_manager = FileManager()
        self.theme = ModernTheme()
        
        # Create main window
        self.view = MainWindow(root, self)
        
        # Initialize state
        self.current_folder = None
        self.current_ignore_folders = []
    
    def load_folder(self, folder_path):
        """Load and display folder structure"""
        if not os.path.exists(folder_path):
            self.update_status("❌ Invalid folder path", self.theme.TEXT_ERROR)
            return
        
        self.update_status(STATUS_LOADING, self.theme.TEXT_ACCENT)
        self.root.update_idletasks()
        
        try:
            self.current_folder = folder_path
            self.current_ignore_folders = self.view.get_header_panel().get_ignore_folders()
            
            # Update all panels
            self.view.get_tree_panel().populate_tree(folder_path, self.current_ignore_folders)
            self.view.get_buttons_panel().populate_buttons(folder_path, self.current_ignore_folders)
            self.view.get_ascii_panel().display_ascii_tree(folder_path, self.current_ignore_folders)
            
            # Get folder stats for progress
            stats = self.file_manager.get_folder_stats(folder_path, self.current_ignore_folders)
            self.view.update_progress(f"{stats['total_files']} files, {stats['total_lines']:,} lines")
            
            self.update_status("✅ Folder loaded successfully!", self.theme.TEXT_SUCCESS)
            self.root.after(3000, lambda: self.update_status(STATUS_READY))
            
        except Exception as e:
            self.update_status(f"❌ Error loading folder: {str(e)}", self.theme.TEXT_ERROR)
    
    def refresh_display(self):
        """Refresh the current display"""
        if not self.current_folder:
            self.update_status("❌ No folder selected", self.theme.TEXT_ERROR)
            return
        
        self.update_status(STATUS_REFRESHING, self.theme.TEXT_ACCENT)
        self.load_folder(self.current_folder)
    
    def copy_single_file(self, file_path):
        """Copy content of a single file to clipboard"""
        try:
            file_name = os.path.basename(file_path)
            content = self.file_manager.get_file_content(file_path)
            lines = self.file_manager.count_lines_of_code(file_path)
            
            # Format content with header
            formatted_content = f"// File: {file_name} ({lines} lines)\n"
            formatted_content += f"// Path: {file_path}\n"
            formatted_content += "// " + "="*78 + "\n\n"
            formatted_content += content
            
            pyperclip.copy(formatted_content)
            self.update_status(f"✅ {file_name} copied to clipboard!", self.theme.TEXT_SUCCESS)
            self.root.after(3000, lambda: self.update_status(STATUS_READY))
            
        except Exception as e:
            self.update_status(f"❌ Error copying file: {str(e)}", self.theme.TEXT_ERROR)
    
    def copy_all_files(self):
        """Copy all files content to clipboard"""
        if not self.current_folder:
            self.update_status("❌ No folder selected", self.theme.TEXT_ERROR)
            return
        
        self.update_status(STATUS_COPYING, self.theme.TEXT_ACCENT)
        self.root.update_idletasks()
        
        try:
            content, file_count = self.file_manager.get_all_files_content(
                self.current_folder, self.current_ignore_folders
            )
            
            if content:
                pyperclip.copy(content)
                self.update_status(f"✅ {file_count} files copied to clipboard!", self.theme.TEXT_SUCCESS)
            else:
                self.update_status("❌ No files to copy", self.theme.TEXT_ERROR)
            
            self.root.after(3000, lambda: self.update_status(STATUS_READY))
            
        except Exception as e:
            self.update_status(f"❌ Error copying files: {str(e)}", self.theme.TEXT_ERROR)
    
    def copy_ascii_tree(self):
        """Copy ASCII tree to clipboard"""
        try:
            content = self.view.get_ascii_panel().get_content()
            if content.strip():
                pyperclip.copy(content)
                self.update_status("✅ ASCII tree copied to clipboard!", self.theme.TEXT_SUCCESS)
                self.root.after(3000, lambda: self.update_status(STATUS_READY))
            else:
                self.update_status("❌ No tree to copy", self.theme.TEXT_ERROR)
        except Exception as e:
            self.update_status(f"❌ Error copying tree: {str(e)}", self.theme.TEXT_ERROR)
    
    def show_statistics(self):
        """Show folder statistics"""
        if not self.current_folder:
            self.update_status("❌ No folder selected", self.theme.TEXT_ERROR)
            return
        
        try:
            stats = self.file_manager.get_folder_stats(self.current_folder, self.current_ignore_folders)
            self.view.show_statistics_dialog(stats)
        except Exception as e:
            self.update_status(f"❌ Error generating statistics: {str(e)}", self.theme.TEXT_ERROR)
    
    def update_status(self, message, color=None):
        """Update status bar"""
        self.view.update_status(message, color)