# File-Organizer
 The Python File Organizer is a practical project designed to automatically arrange files in a folder into neatly named category-based subfolders.


# Python File Organizer

A simple Python project that sorts files into folders like `Images`, `Documents`, `Videos`, `Music`, `Archives`, `Code`, and `Others`.

## Features

- Organizes files in any folder you choose
- Supports a safe `--dry-run` preview mode
- Avoids overwriting duplicate names by renaming files
- Keeps existing folders untouched

## Run

```bash
python file_organizer.py --dry-run
python file_organizer.py
python file_organizer.py "C:\path\to\your\folder"
```

## Example

If a folder contains:

- `photo.jpg`
- `report.pdf`
- `song.mp3`

After running the script, it becomes:

- `Images/photo.jpg`
- `Documents/report.pdf`
- `Music/song.mp3`
