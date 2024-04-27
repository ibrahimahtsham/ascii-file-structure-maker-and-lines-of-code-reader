import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pyperclip  # Module for copying text to clipboard


def count_lines_of_code(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return sum(1 for line in file)
    except UnicodeDecodeError:
        return 0  # Return 0 lines for files with decoding errors


def generate_ascii_tree(folder_path, ignore_folders=[], indent=""):
    tree = ""
    total_lines = 0
    items = os.listdir(folder_path)
    for i, item in enumerate(items):
        if item in ignore_folders:
            continue
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            if i == len(items) - 1:
                subtree, subtree_lines = generate_ascii_tree(
                    item_path, ignore_folders, indent + "    "
                )
                tree += (
                    indent
                    + "└── "
                    + item
                    + " (Total Lines: "
                    + str(subtree_lines)
                    + ")\n"
                    + subtree
                )
            else:
                subtree, subtree_lines = generate_ascii_tree(
                    item_path, ignore_folders, indent + "│   "
                )
                tree += (
                    indent
                    + "├── "
                    + item
                    + " (Total Lines: "
                    + str(subtree_lines)
                    + ")\n"
                    + subtree
                )
            total_lines += subtree_lines
        else:
            lines_of_code = count_lines_of_code(item_path)
            total_lines += lines_of_code
            if i == len(items) - 1:
                tree += (
                    indent + "└── " + item + " (Lines: " + str(lines_of_code) + ")\n"
                )
            else:
                tree += (
                    indent + "├── " + item + " (Lines: " + str(lines_of_code) + ")\n"
                )
    return tree, total_lines


def display_file_structure(folder_path, tree):
    clear_buttons_frame()
    tree.delete(*tree.get_children())
    root_node = tree.insert("", "end", text=folder_path, open=True)
    ignore_folders = ignore_var.get().split(",")
    _populate_tree(folder_path, root_node, tree, ignore_folders)


def clear_buttons_frame():
    for widget in buttons_inner_frame.winfo_children():
        widget.destroy()


def _populate_tree(folder_path, parent, tree, ignore_folders=[]):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            if item not in ignore_folders:
                node = tree.insert(parent, "end", text=item, open=False)
                _populate_tree(item_path, node, tree, ignore_folders)
        else:
            file_node = tree.insert(parent, "end", text=item)
            button_text = "Copy " + item
            copy_button = tk.Button(
                buttons_inner_frame,
                text=button_text,
                command=lambda path=item_path: copy_file_content_to_clipboard(path),
                bg="#606060",
                fg="#ffffff",
                activebackground="#4c4c4c",
                activeforeground="#ffffff",
            )
            copy_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)


def copy_file_content_to_clipboard(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
        pyperclip.copy(file_content)
        print("File content copied to clipboard.")


def display_ascii_tree(folder_path, ignore_folders=[]):
    ascii_tree, total_lines = generate_ascii_tree(folder_path, ignore_folders)
    ascii_tree_text.delete(1.0, tk.END)
    ascii_tree_text.insert(tk.END, ascii_tree)
    ascii_tree_text.insert(tk.END, "\nTotal Lines in Folder: " + str(total_lines))


def copy_files_content(folder_path, ignore_folders=[]):
    file_contents = ""
    for root, dirs, files in os.walk(folder_path):
        # Exclude files in ignore folders
        files = [
            file
            for file in files
            if not any(
                ignore_folder in os.path.join(root, file)
                for ignore_folder in ignore_folders
            )
        ]
        for file in files:
            file_path = os.path.join(root, file)
            lines_of_code = count_lines_of_code(file_path)
            if lines_of_code > 0:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    file_contents += f"Code for {file}:\n\n"  # Add filename as header
                    file_contents += f.read() + "\n\n"
    pyperclip.copy(file_contents)


def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_var.set(folder_path)
        display_file_structure(folder_path, file_tree)
        ignore_folders = ignore_var.get().split(",")
        display_ascii_tree(folder_path, ignore_folders)


def refresh_display():
    folder_path = folder_var.get()
    if folder_path:
        clear_buttons_frame()
        ignore_folders = ignore_var.get().split(",")
        display_file_structure(folder_path, file_tree)
        display_ascii_tree(folder_path, ignore_folders)


def copy_files():
    folder_path = folder_var.get()
    if folder_path:
        ignore_folders = ignore_var.get().split(",")
        copy_files_content(folder_path, ignore_folders)
        print("Files content copied to clipboard.")


# GUI setup
root = tk.Tk()
root.title("File Structure Viewer")

# Set window state to maximized
root.state("zoomed")

# Dark mode color scheme
root.configure(bg="#1e1e1e")
tk_style = ttk.Style()
tk_style.theme_use("clam")
tk_style.configure(
    "Treeview", background="#3c3f41", foreground="#ffffff", fieldbackground="#3c3f41"
)
tk_style.map("Treeview", background=[("selected", "#606060"), ("active", "#606060")])
tk_style.configure(
    "Treeview", background="#3c3f41", foreground="#ffffff", fieldbackground="#3c3f41"
)
tk_style.configure("Treeview.Heading", background="#282828", foreground="#ffffff")
tk_style.configure("TButton", background="#606060", foreground="#ffffff")
tk_style.configure("TEntry", fieldbackground="#464646", foreground="#ffffff")
tk_style.map(
    "TButton", background=[("active", "#4c4c4c")], foreground=[("active", "#ffffff")]
)

# Create a frame for the header
header_frame = tk.Frame(root, bg="#1e1e1e")
header_frame.pack(fill=tk.X)

# Folder selection
folder_label = tk.Label(header_frame, text="Select Folder:", bg="#1e1e1e", fg="#ffffff")
folder_label.pack(side=tk.LEFT, padx=(5, 0), pady=5)

folder_var = tk.StringVar()
folder_entry = tk.Entry(
    header_frame, textvariable=folder_var, bg="#464646", fg="#ffffff"
)
folder_entry.config(insertbackground="white")
folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

browse_button = tk.Button(
    header_frame, text="Browse", command=browse_folder, bg="#606060", fg="#ffffff"
)
browse_button.pack(side=tk.LEFT, padx=5, pady=5)

# Ignore folders entry
ignore_label = tk.Label(
    header_frame, text="Ignore Folders (comma-separated):", bg="#1e1e1e", fg="#ffffff"
)
ignore_label.pack(side=tk.LEFT, padx=(20, 0), pady=5)

ignore_var = tk.StringVar()
ignore_var.set(
    ".git,.gitignore,.expo,node_modules,.idea,.svg,.eslintrc.cjs,package-lock.json,package.json,app.json,babel.config.js,eas.json,vite.config.js"
)  # Set initial value
ignore_entry = tk.Entry(
    header_frame, textvariable=ignore_var, bg="#464646", fg="#ffffff"
)
ignore_entry.config(insertbackground="white")
ignore_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

refresh_button = tk.Button(
    header_frame,
    text="Refresh",
    command=refresh_display,
    bg="#606060",
    fg="#ffffff",
    activebackground="#4c4c4c",
    activeforeground="#ffffff",
)
refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

# Copy files button
copy_button = tk.Button(
    header_frame,
    text="Copy All Files",
    command=copy_files,
    bg="#606060",
    fg="#ffffff",
    activebackground="#4c4c4c",
    activeforeground="#ffffff",
)
copy_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a PanedWindow for resizable sidebar
main_paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
main_paned_window.pack(expand=True, fill=tk.BOTH, padx=10, pady=(0, 10))

# Container for file structure display
tree_frame = tk.Frame(main_paned_window)
tree_frame.pack(fill=tk.BOTH, expand=True)

# Treeview for file structure display
file_tree_frame = ttk.Frame(tree_frame)
file_tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

file_tree_scroll = ttk.Scrollbar(file_tree_frame)
file_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

file_tree = ttk.Treeview(file_tree_frame, yscrollcommand=file_tree_scroll.set)
file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

file_tree_scroll.config(command=file_tree.yview)

main_paned_window.add(tree_frame)

# Buttons container
buttons_frame = tk.Frame(main_paned_window, bg="#1e1e1e")  # Set background color
buttons_frame.pack(fill=tk.BOTH, expand=True)

# Add a canvas for the buttons container with scrollbar
buttons_canvas = tk.Canvas(buttons_frame, bg="#1e1e1e")  # Set background color
buttons_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

buttons_scroll = ttk.Scrollbar(
    buttons_frame, orient=tk.VERTICAL, command=buttons_canvas.yview
)
buttons_scroll.pack(side=tk.RIGHT, fill=tk.Y)

buttons_inner_frame = tk.Frame(buttons_canvas, bg="#1e1e1e")  # Set background color
buttons_canvas.create_window((0, 0), window=buttons_inner_frame, anchor=tk.NW)

buttons_inner_frame.bind(
    "<Configure>",
    lambda e: buttons_canvas.configure(scrollregion=buttons_canvas.bbox("all")),
)
buttons_canvas.configure(yscrollcommand=buttons_scroll.set)

main_paned_window.add(buttons_frame)


# ASCII file structure display
ascii_tree_frame = tk.Frame(main_paned_window)
ascii_tree_frame.pack(fill=tk.BOTH, expand=True)

ascii_tree_text = tk.Text(
    ascii_tree_frame, wrap=tk.WORD, width=80, height=20, bg="#1e1e1e", fg="#ffffff"
)
ascii_tree_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

text_scroll = ttk.Scrollbar(
    ascii_tree_frame, orient=tk.VERTICAL, command=ascii_tree_text.yview
)
text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the yscrollcommand of the Text widget
ascii_tree_text.config(yscrollcommand=text_scroll.set)

# Change cursor color to white
ascii_tree_text.config(insertbackground="white")

main_paned_window.add(ascii_tree_frame)


root.mainloop()
