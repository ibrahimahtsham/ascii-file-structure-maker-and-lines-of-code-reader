"""
Modern dark theme configuration with improved colors and styling
"""

class ModernTheme:
    # Base colors
    BACKGROUND_PRIMARY = "#1e1e1e"      # Main background
    BACKGROUND_SECONDARY = "#2d2d2d"    # Secondary panels
    BACKGROUND_TERTIARY = "#3a3a3a"     # Input fields, buttons
    
    # Accent colors
    ACCENT_BLUE = "#007acc"             # Primary action color
    ACCENT_BLUE_HOVER = "#005a9e"       # Hover state
    ACCENT_GREEN = "#28a745"            # Success color
    ACCENT_ORANGE = "#fd7e14"           # Warning color
    ACCENT_RED = "#dc3545"              # Error color
    ACCENT_PURPLE = "#6f42c1"           # Secondary action
    
    # Text colors
    TEXT_PRIMARY = "#ffffff"            # Primary text
    TEXT_SECONDARY = "#b0b0b0"          # Secondary text
    TEXT_ACCENT = "#ffd700"             # Accent text (folder totals)
    TEXT_SUCCESS = "#40ff40"            # File counts
    TEXT_ERROR = "#ff4444"              # Error messages
    
    # Tree colors
    TREE_FOLDER = "#ffa726"             # Folder color
    TREE_FILE = "#66bb6a"               # File color
    TREE_ERROR = "#f44336"              # Error color
    
    # Borders and shadows
    BORDER_COLOR = "#404040"
    SHADOW_COLOR = "#000000"
    
    # Fonts
    FONT_FAMILY = "Segoe UI"
    FONT_MONO = "Consolas"
    
    @staticmethod
    def get_button_style(color, hover_color=None):
        """Get button styling configuration"""
        return {
            'bg': color,
            'fg': ModernTheme.TEXT_PRIMARY,
            'activebackground': hover_color or color,
            'activeforeground': ModernTheme.TEXT_PRIMARY,
            'font': (ModernTheme.FONT_FAMILY, 10, "bold"),
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 20,
            'pady': 8
        }
    
    @staticmethod
    def get_entry_style():
        """Get entry field styling"""
        return {
            'bg': ModernTheme.BACKGROUND_TERTIARY,
            'fg': ModernTheme.TEXT_PRIMARY,
            'insertbackground': ModernTheme.TEXT_PRIMARY,
            'relief': 'flat',
            'font': (ModernTheme.FONT_MONO, 10)
        }
    
    @staticmethod
    def get_label_style(size=10, weight="normal"):
        """Get label styling"""
        return {
            'bg': ModernTheme.BACKGROUND_SECONDARY,
            'fg': ModernTheme.TEXT_PRIMARY,
            'font': (ModernTheme.FONT_FAMILY, size, weight)
        }