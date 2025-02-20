from pathlib import Path
import shutil

# Define file categories and their corresponding extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv"],
    "Music": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".java"]
}

def sort_files(source_folder):
    """
    Sorts files in the specified folder into categorized subfolders.
    """
    source = Path(source_folder)

    if not source.exists():
        print(f"Error: The folder '{source_folder}' does not exist.")
        return

    for file in source.iterdir():
        if file.is_file():  # Ignore directories
            file_extension = file.suffix.lower()

            # Determine the file category
            category = next((cat for cat, ext in FILE_CATEGORIES.items() if file_extension in ext), "Other")

            # Create category folder if it doesn't exist
            category_folder = source / category
            category_folder.mkdir(exist_ok=True)

            # Move file to the corresponding folder
            try:
                shutil.move(str(file), str(category_folder / file.name))
                print(f"Moved: {file.name} -> {category}/")
            except Exception as e:
                print(f"Error moving {file.name}: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path to sort: ").strip()
    sort_files(folder_path)
