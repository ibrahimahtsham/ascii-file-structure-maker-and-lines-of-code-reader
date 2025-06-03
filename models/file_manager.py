"""
File management and processing logic
"""
import os
from typing import List, Tuple, Dict

class FileManager:
    def __init__(self):
        self.file_cache = {}
    
    def count_lines_of_code(self, file_path: str) -> int:
        """Count lines of code in a file with caching"""
        if file_path in self.file_cache:
            return self.file_cache[file_path]
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = sum(1 for line in file)
                self.file_cache[file_path] = lines
                return lines
        except (UnicodeDecodeError, PermissionError, FileNotFoundError):
            self.file_cache[file_path] = 0
            return 0
    
    def generate_ascii_tree(self, folder_path: str, ignore_folders: List[str] = None, indent: str = "") -> Tuple[str, int]:
        """Generate ASCII tree representation of folder structure"""
        if ignore_folders is None:
            ignore_folders = []
        
        tree = ""
        total_lines = 0
        
        try:
            items = os.listdir(folder_path)
        except PermissionError:
            return "Permission denied", 0
        
        # Filter ignored folders and sort items
        items = [item for item in items if item not in ignore_folders]
        items.sort(key=lambda x: (os.path.isfile(os.path.join(folder_path, x)), x.lower()))
        
        for i, item in enumerate(items):
            item_path = os.path.join(folder_path, item)
            is_last = i == len(items) - 1
            
            if os.path.isdir(item_path):
                connector = "└── " if is_last else "├── "
                next_indent = indent + ("    " if is_last else "│   ")
                
                subtree, subtree_lines = self.generate_ascii_tree(item_path, ignore_folders, next_indent)
                
                tree += f"{indent}{connector}📁 {item} 🔢({subtree_lines} total lines)\n{subtree}"
                total_lines += subtree_lines
            else:
                lines_of_code = self.count_lines_of_code(item_path)
                total_lines += lines_of_code
                connector = "└── " if is_last else "├── "
                
                tree += f"{indent}{connector}📄 {item} 📊({lines_of_code} lines)\n"
        
        return tree, total_lines
    
    def get_file_content(self, file_path: str) -> str:
        """Get content of a file"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def get_all_files_content(self, folder_path: str, ignore_folders: List[str] = None) -> Tuple[str, int]:
        """Get content of all files in folder"""
        if ignore_folders is None:
            ignore_folders = []
        
        file_contents = ""
        file_count = 0
        
        for root, dirs, files in os.walk(folder_path):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_folders]
            
            for file in files:
                file_path = os.path.join(root, file)
                lines_of_code = self.count_lines_of_code(file_path)
                
                if lines_of_code > 0:
                    try:
                        content = self.get_file_content(file_path)
                        relative_path = os.path.relpath(file_path, folder_path)
                        file_contents += f"// File: {relative_path} ({lines_of_code} lines)\n"
                        file_contents += content + "\n\n" + "="*80 + "\n\n"
                        file_count += 1
                    except Exception:
                        continue
        
        return file_contents, file_count
    
    def get_folder_stats(self, folder_path: str, ignore_folders: List[str] = None) -> Dict:
        """Get comprehensive folder statistics"""
        if ignore_folders is None:
            ignore_folders = []
        
        stats = {
            'total_files': 0,
            'total_lines': 0,
            'file_types': {},
            'folder_count': 0
        }
        
        for root, dirs, files in os.walk(folder_path):
            dirs[:] = [d for d in dirs if d not in ignore_folders]
            stats['folder_count'] += len(dirs)
            
            for file in files:
                file_path = os.path.join(root, file)
                lines = self.count_lines_of_code(file_path)
                
                if lines > 0:
                    stats['total_files'] += 1
                    stats['total_lines'] += lines
                    
                    # Track file extensions
                    ext = os.path.splitext(file)[1].lower()
                    if ext:
                        stats['file_types'][ext] = stats['file_types'].get(ext, 0) + 1
        
        return stats