🗂 File Organizer Script

A Python script that automatically sorts files into categorized folders based on file extensions. Includes a GUI for easy use and can be packaged as a standalone .exe.
✨ Features

✔ Automatically organizes files into predefined folders (Images, Documents, Videos, etc.).
✔ GUI for selecting folders and tracking progress.
✔ Undo function to revert last sorting action.
✔ Error handling for duplicate files & invalid paths.
✔ Can be compiled into an .exe with PyInstaller.
🚀 How to Use

    Run the script (file_sorter.py).
    Select a folder to organize or press Enter to use the current directory.
    Click Start Sorting – files will be moved to their respective folders.
    Use Undo if needed.

🔧 Requirements

    Python 3.11+
    pathlib, shutil, tkinter (included in Python standard library)

🏗 Build as an .exe

To create a standalone executable (Windows):

pyinstaller --onefile --windowed file_sorter.py

📦 Future Improvements

    Progress bar for better UI feedback
    Sorting based on file size or date
    Multi-threading for large file batches

📌 Developed for personal automation & learning GUI integration in Python! 🚀
