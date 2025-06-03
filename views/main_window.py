"""
Main application window
"""
import tkinter as tk
from tkinter import ttk, messagebox
from utils.theme import ModernTheme
from utils.constants import WINDOW_TITLE, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from views.components.header_panel import HeaderPanel
from views.components.tree_panel import TreePanel
from views.components.buttons_panel import ButtonsPanel
from views.components.ascii_panel import AsciiPanel

class MainWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.theme = ModernTheme()
        
        self.setup_window()
        self.setup_styles()
        self.create_layout()
        self.create_status_bar()
    
    def setup_window(self):
        """Configure main window"""
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_MIN_WIDTH}x{WINDOW_MIN_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.root.configure(bg=self.theme.BACKGROUND_PRIMARY)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_MIN_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (WINDOW_MIN_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_MIN_WIDTH}x{WINDOW_MIN_HEIGHT}+{x}+{y}")
        
        # Configure window icon (if you have one)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure Treeview
        style.configure(
            "Treeview",
            background=self.theme.BACKGROUND_PRIMARY,
            foreground=self.theme.TEXT_PRIMARY,
            fieldbackground=self.theme.BACKGROUND_PRIMARY,
            borderwidth=0
        )
        style.map(
            "Treeview",
            background=[("selected", self.theme.ACCENT_BLUE)],
            foreground=[("selected", self.theme.TEXT_PRIMARY)]
        )
        
        # Configure PanedWindow
        style.configure(
            "TPanedwindow",
            background=self.theme.BACKGROUND_PRIMARY
        )
        
        # Configure Scrollbar
        style.configure(
            "Vertical.TScrollbar",
            background=self.theme.BACKGROUND_TERTIARY,
            troughcolor=self.theme.BACKGROUND_PRIMARY,
            borderwidth=0,
            arrowcolor=self.theme.TEXT_SECONDARY
        )
    
    def create_layout(self):
        """Create main application layout"""
        # Header panel
        self.header_panel = HeaderPanel(self.root, self.controller)
        
        # Main content area with paned window
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(expand=True, fill=tk.BOTH, padx=15, pady=(10, 0))
        
        # Create panels
        self.tree_panel = TreePanel(self.main_paned, self.controller)
        self.buttons_panel = ButtonsPanel(self.main_paned, self.controller)
        self.ascii_panel = AsciiPanel(self.main_paned, self.controller)
        
        # Add panels to paned window
        self.main_paned.add(self.tree_panel.get_frame(), weight=1)
        self.main_paned.add(self.buttons_panel.get_frame(), weight=1)
        self.main_paned.add(self.ascii_panel.get_frame(), weight=2)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_frame = tk.Frame(
            self.root,
            bg=self.theme.BACKGROUND_TERTIARY,
            height=35
        )
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            bg=self.theme.BACKGROUND_TERTIARY,
            fg=self.theme.TEXT_PRIMARY,
            font=(self.theme.FONT_FAMILY, 9),
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, padx=15, pady=8)
        
        # Progress indicator (optional)
        self.progress_var = tk.StringVar()
        self.progress_label = tk.Label(
            self.status_frame,
            textvariable=self.progress_var,
            bg=self.theme.BACKGROUND_TERTIARY,
            fg=self.theme.TEXT_SECONDARY,
            font=(self.theme.FONT_FAMILY, 9)
        )
        self.progress_label.pack(side=tk.RIGHT, padx=15, pady=8)
    
    def update_status(self, message, color=None):
        """Update status bar message"""
        if color is None:
            color = self.theme.TEXT_PRIMARY
        
        self.status_label.config(text=message, fg=color)
        self.root.update_idletasks()
    
    def update_progress(self, message=""):
        """Update progress indicator"""
        self.progress_var.set(message)
        self.root.update_idletasks()
    
    def show_statistics_dialog(self, stats):
        """Show folder statistics in a modal dialog that can be closed by clicking outside"""
        # Create overlay frame that covers the entire window
        self.overlay_frame = tk.Frame(
            self.root,
            bg='black'
        )
        self.overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay_frame.configure(bg='black')
        
        # Make overlay semi-transparent effect by using a dark color
        self.overlay_frame.configure(bg='#000000')
        
        # Bind click on overlay to close dialog
        self.overlay_frame.bind('<Button-1>', lambda e: self.close_statistics_dialog())
        
        # Create the actual dialog window
        self.stats_window = tk.Frame(
            self.overlay_frame,
            bg=self.theme.BACKGROUND_SECONDARY,
            relief='raised',
            borderwidth=2
        )
        
        # Center the dialog
        dialog_width = 500
        dialog_height = 400
        x = (self.root.winfo_width() - dialog_width) // 2
        y = (self.root.winfo_height() - dialog_height) // 2
        
        self.stats_window.place(x=x, y=y, width=dialog_width, height=dialog_height)
        
        # Prevent dialog from closing when clicked
        self.stats_window.bind('<Button-1>', lambda e: "break")
        
        # Title
        title_label = tk.Label(
            self.stats_window,
            text="📊 Folder Statistics",
            **self.theme.get_label_style(14, "bold")
        )
        title_label.pack(pady=20)
        
        # Statistics content frame
        content_frame = tk.Frame(self.stats_window, bg=self.theme.BACKGROUND_SECONDARY)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=(0, 20))
        
        # Statistics text
        stats_text = tk.Text(
            content_frame,
            bg=self.theme.BACKGROUND_PRIMARY,
            fg=self.theme.TEXT_PRIMARY,
            font=(self.theme.FONT_MONO, 10),
            relief="flat",
            padx=20,
            pady=20
        )
        stats_text.pack(expand=True, fill=tk.BOTH)
        
        # Format statistics
        content = f"""Total Files: {stats['total_files']:,}
Total Lines of Code: {stats['total_lines']:,}
Total Folders: {stats['folder_count']:,}

File Types:
"""
        for ext, count in sorted(stats['file_types'].items()):
            content += f"  {ext}: {count} files\n"
        
        stats_text.insert(tk.END, content)
        stats_text.config(state=tk.DISABLED)
        
        # Button frame
        button_frame = tk.Frame(self.stats_window, bg=self.theme.BACKGROUND_SECONDARY)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Close button
        close_button = tk.Button(
            button_frame,
            text="Close",
            command=self.close_statistics_dialog,
            **self.theme.get_button_style(self.theme.ACCENT_BLUE)
        )
        close_button.pack(side=tk.RIGHT)
        
        # Info label
        info_label = tk.Label(
            button_frame,
            text="Click outside to close",
            bg=self.theme.BACKGROUND_SECONDARY,
            fg=self.theme.TEXT_SECONDARY,
            font=(self.theme.FONT_FAMILY, 8)
        )
        info_label.pack(side=tk.LEFT)

    def close_statistics_dialog(self):
        """Close the statistics dialog"""
        if hasattr(self, 'overlay_frame'):
            self.overlay_frame.destroy()
            delattr(self, 'overlay_frame')
        if hasattr(self, 'stats_window'):
            delattr(self, 'stats_window')

    def get_header_panel(self):
        """Get header panel reference"""
        return self.header_panel
    
    def get_tree_panel(self):
        """Get tree panel reference"""
        return self.tree_panel
    
    def get_buttons_panel(self):
        """Get buttons panel reference"""
        return self.buttons_panel
    
    def get_ascii_panel(self):
        """Get ASCII panel reference"""
        return self.ascii_panel