#!/usr/bin/env python3
import shutil
from pathlib import Path

# Dictionary mapping folder names to lists of file extensions
FOLDER_MAP = {
    "Images": [".jpg", ".jpeg", ".png"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Videos": [".mp4", ".mov", ".avi", ".gif"],
}

def setup_folders(directory: Path):
    """
    Ensure that each folder in FOLDER_MAP exists under 'directory'.
    Also creates a 'Misc' folder for any uncategorized files.
    Print a message indicating whether the folder was created or already exists.
    """
    for folder_name in FOLDER_MAP.keys():
        folder_path = directory / folder_name
        if folder_path.exists():
            print(f"Folder '{folder_path.name}' already exists.")
        else:
            folder_path.mkdir(exist_ok=True)
            print(f"Created folder '{folder_path.name}'.")

    # Create a 'Misc' folder too
    misc_folder = directory / "Misc"
    if misc_folder.exists():
        print(f"Folder '{misc_folder.name}' already exists.")
    else:
        misc_folder.mkdir(exist_ok=True)
        print(f"Created folder '{misc_folder.name}'.")

def organize_files(directory: Path):
    """
    Move files in 'directory' into pre-created subfolders based on extension.
    Files whose extensions aren't listed in FOLDER_MAP go to 'Misc'.
    """
    if not directory.is_dir():
        print(f"Error: {directory} is not a valid directory.")
        return

    # Set up the folders before sorting
    setup_folders(directory)

    # Iterate over items in the directory
    for file_path in directory.iterdir():
        # Skip directories (including the newly created ones)
        if file_path.is_dir():
            continue

        # Skip the organizer script itself
        if file_path.name == "file_sorter.py":
            print(f"Skipping {file_path.name} (the organizer script).")
            continue

        # Skip other files you don't want moved
        if file_path.name == "requirements.txt":
            print(f"Skipping {file_path.name} (requirements file).")
            continue

        # Identify which folder this file should go in, based on extension
        file_extension = file_path.suffix.lower()  # e.g., ".jpg"
        destination_folder = None

        # Check each folder in FOLDER_MAP to see if the extension is listed
        for folder_name, extensions in FOLDER_MAP.items():
            if file_extension in extensions:
                destination_folder = directory / folder_name
                break

        # If no match is found, place the file in 'Misc'
        if not destination_folder:
            destination_folder = directory / "Misc"

        final_path = destination_folder / file_path.name

        # If a file with the same name already exists, skip it
        if final_path.exists():
            print(f"Skipping {file_path.name}, already exists in {destination_folder.name}.")
            continue

        try:
            shutil.move(str(file_path), str(destination_folder))
            print(f"Moved {file_path.name} -> {destination_folder.name}")
        except PermissionError:
            print(f"Permission error while moving {file_path.name}.")
        except Exception as e:
            print(f"Error moving {file_path.name}: {e}")

def main():
    folder_to_organize = input("Enter the path of the folder you want to organize: ")
    directory = Path(folder_to_organize.strip())

    organize_files(directory)

if __name__ == "__main__":
    main()
