"""
File Structure Viewer v3.0
Modern MVC Architecture Implementation
"""
import tkinter as tk
from controllers.main_controller import MainController

def main():
    root = tk.Tk()
    app = MainController(root)
    root.mainloop()

if __name__ == "__main__":
    main()