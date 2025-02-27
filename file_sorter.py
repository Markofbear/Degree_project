#!/usr/bin/env python3
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

# Dictionary mapping folder names to lists of file extensions
FOLDER_MAP = {
    "Images": [".jpg", ".jpeg", ".png"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Videos": [".mp4", ".mov", ".avi", ".gif"],
}

# Stack to track file movements for undo functionality
undo_stack = []

def setup_folders(directory: Path, log):
    """Ensure required folders exist. Log actions in GUI."""
    for folder_name in FOLDER_MAP.keys():
        folder_path = directory / folder_name
        if not folder_path.exists():
            folder_path.mkdir(exist_ok=True)
            log.insert(tk.END, f"Created folder '{folder_path.name}'\n")
        else:
            log.insert(tk.END, f"Folder '{folder_path.name}' already exists\n")

    # Create "Misc" folder for unlisted file types
    misc_folder = directory / "Misc"
    if not misc_folder.exists():
        misc_folder.mkdir(exist_ok=True)
        log.insert(tk.END, "Created folder 'Misc'\n")
    else:
        log.insert(tk.END, "Folder 'Misc' already exists\n")

def organize_files(directory: Path, log):
    """Move files into categorized folders and log actions."""
    global undo_stack
    undo_stack.clear()  # Clear previous undo history

    if not directory.is_dir():
        messagebox.showerror("Error", f"'{directory}' is not a valid directory.")
        return

    setup_folders(directory, log)

    for file_path in directory.iterdir():
        if file_path.is_dir():
            continue

        if file_path.name in ["file_sorter.py", "requirements.txt"]:
            log.insert(tk.END, f"Skipping {file_path.name} (system file)\n")
            continue

        file_extension = file_path.suffix.lower()
        destination_folder = None

        for folder_name, extensions in FOLDER_MAP.items():
            if file_extension in extensions:
                destination_folder = directory / folder_name
                break

        if not destination_folder:
            destination_folder = directory / "Misc"

        final_path = destination_folder / file_path.name

        if final_path.exists():
            log.insert(tk.END, f"Skipping {file_path.name}, already exists in {destination_folder.name}\n")
            continue

        try:
            shutil.move(str(file_path), str(destination_folder))
            undo_stack.append((final_path, file_path))  # Store the original and new locations
            log.insert(tk.END, f"Moved {file_path.name} -> {destination_folder.name}\n")
        except PermissionError:
            log.insert(tk.END, f"Permission error while moving {file_path.name}\n")
        except Exception as e:
            log.insert(tk.END, f"Error moving {file_path.name}: {e}\n")

    messagebox.showinfo("Success", "File organization completed!")

def undo_last_action(log):
    """Move files back to their original locations."""
    global undo_stack

    if not undo_stack:
        messagebox.showwarning("Undo", "No actions to undo.")
        return

    while undo_stack:
        moved_file, original_location = undo_stack.pop()
        try:
            shutil.move(str(moved_file), str(original_location))
            log.insert(tk.END, f"Reverted {moved_file.name} back to {original_location.parent.name}\n")
        except Exception as e:
            log.insert(tk.END, f"Error undoing {moved_file.name}: {e}\n")

    messagebox.showinfo("Undo", "All actions have been undone.")

def select_folder(entry_field):
    """Open folder selection dialog and update entry field."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, folder_selected)

def start_sorting(entry_field, log):
    """Trigger file organization from GUI."""
    folder_path = Path(entry_field.get().strip())
    if not folder_path.exists():
        messagebox.showerror("Error", "Invalid folder path. Please select a valid folder.")
        return

    log.delete(1.0, tk.END)
    organize_files(folder_path, log)

# GUI Implementation
root = tk.Tk()
root.title("File Sorter")
root.geometry("500x450")

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(frame, text="Select folder to organize:")
label.pack()

entry = tk.Entry(frame, width=50)
entry.pack()

browse_button = tk.Button(frame, text="Browse", command=lambda: select_folder(entry))
browse_button.pack(pady=5)

sort_button = tk.Button(frame, text="Start Sorting", command=lambda: start_sorting(entry, log))
sort_button.pack(pady=5)

undo_button = tk.Button(frame, text="Undo", command=lambda: undo_last_action(log))
undo_button.pack(pady=5)

log_label = tk.Label(root, text="Sorting Log:")
log_label.pack()

log = tk.Text(root, height=10, width=60)
log.pack()

root.mainloop()
