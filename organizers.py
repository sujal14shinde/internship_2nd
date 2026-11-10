import os
import shutil
from pathlib import Path

# Extension mapping dictionary
EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".xls": "Documents", ".xlsx": "Documents",
    ".csv": "Documents", ".ppt": "Documents", ".pptx": "Documents",
    ".odt": "Documents", ".rtf": "Documents",
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
    ".gif": "Images", ".bmp": "Images", ".svg": "Images",
    ".webp": "Images", ".heic": "Images",
    # Videos
    ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos",
    ".avi": "Videos", ".wmv": "Videos", ".flv": "Videos", ".webm": "Videos",
    # Audio
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio",
    ".aac": "Audio", ".ogg": "Audio", ".m4a": "Audio",
    # Archives
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives",
    ".tar": "Archives", ".gz": "Archives",
    # Code
    ".py": "Code", ".js": "Code", ".html": "Code", ".css": "Code",
    ".java": "Code", ".cpp": "Code", ".c": "Code", ".json": "Code",
    # Apps
    ".exe": "Apps", ".msi": "Apps", ".apk": "Apps",
}

def get_unique_path(destination: Path) -> Path:
    """Naming collision handle: file.txt -> file (1).txt"""
    if not destination.exists():
        return destination
    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent
    counter = 1
    while True:
        new_name = f"{stem} ({counter}){suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1

def organize_folder(target_folder):
    target = Path(target_folder).expanduser().resolve()

    if not target.exists() or not target.is_dir():
        print(f"Error: Folder not found -> {target}")
        return

    print("=" * 60)
    print("  AUTOMATED FILE ORGANIZER & CLEANUP UTILITY")
    print("=" * 60)
    print(f"Target Folder: {target}\n")

    moved = 0
    skipped = 0
    errors = 0
    summary = {}

    # Use os.scandir() to inspect files
    try:
        with os.scandir(target) as entries:
            files = [e for e in entries if e.is_file()]
    except PermissionError:
        print(f"Permission denied: Cannot access {target}")
        return

    if not files:
        print("Folder already clean. No files to organize.")
        return

    for entry in files:
        file_path = Path(entry.path)

        # Skip this script itself
        if file_path.name == "organizer.py":
            skipped += 1
            continue

        ext = file_path.suffix.lower()
        category = EXTENSION_MAP.get(ext, "Others")

        # Dynamically create category subfolder
        category_folder = target / category
        try:
            category_folder.mkdir(exist_ok=True)
        except PermissionError:
            print(f"Permission Error: Cannot create folder {category_folder}")
            errors += 1
            continue

        dest_path = category_folder / file_path.name
        dest_path = get_unique_path(dest_path)

        # Safely move with try-except
        try:
            shutil.move(str(file_path), str(dest_path))
            print(f"Moved: {file_path.name:30} -> {category}/")
            moved += 1
            summary[category] = summary.get(category, 0) + 1
        except PermissionError:
            print(f"Permission Error: Cannot move {file_path.name} (file in use / no access)")
            errors += 1
        except FileExistsError:
            print(f"File Exists: Skipped {file_path.name}")
            skipped += 1
        except Exception as e:
            print(f"Error moving {file_path.name}: {e}")
            errors += 1

    # Formatted execution summary
    print("\n" + "=" * 60)
    print("  EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Total files scanned : {len(files)}")
    print(f"Total files moved   : {moved}")
    print(f"Total files skipped : {skipped}")
    print(f"Total errors        : {errors}")
    print("-" * 60)
    for cat, count in summary.items():
        print(f"  {cat:<12} : {count} file(s)")
    print("=" * 60)
    print("Done! Folder organized successfully.")

if __name__ == "__main__":
    print("Press Enter to organize Downloads folder, or type a folder path.")
    print("Example: C:\\Users\\YourName\\Downloads  OR  /home/user/Downloads")
    user_input = input("\nEnter folder path (default: Downloads): ").strip()

    if not user_input:
        default = Path.home() / "Downloads"
        organize_folder(default)
    else:
        organize_folder(user_input)