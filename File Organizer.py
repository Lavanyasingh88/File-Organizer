
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv"},
    "Music": {".mp3", ".wav", ".aac", ".flac", ".ogg"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".json", ".xml"},
}


def get_category(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Others"


def unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination

    counter = 1
    while True:
        candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize_folder(target_dir: Path, dry_run: bool) -> tuple[int, int]:
    moved_count = 0
    skipped_count = 0
    protected_files = {
        Path(__file__).resolve(),
        (Path(__file__).resolve().parent / "README.md").resolve(),
    }

    for item in target_dir.iterdir():
        if item.is_dir():
            continue
        if item.resolve() in protected_files:
            print(f"Skipped: {item.name} (project file)")
            skipped_count += 1
            continue

        category = get_category(item)
        category_dir = target_dir / category
        destination = unique_destination(category_dir / item.name)

        if dry_run:
            print(f"[DRY RUN] {item.name} -> {category}\\{destination.name}")
            moved_count += 1
            continue

        category_dir.mkdir(exist_ok=True)
        try:
            shutil.move(str(item), str(destination))
            print(f"Moved: {item.name} -> {category}\\{destination.name}")
            moved_count += 1
        except OSError as exc:
            print(f"Skipped: {item.name} ({exc})")
            skipped_count += 1

    return moved_count, skipped_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Organize files in a folder into category-based subfolders."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder to organize. Defaults to the current folder.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the moves without changing any files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_dir = Path(args.folder).expanduser().resolve()

    if not target_dir.exists() or not target_dir.is_dir():
        raise SystemExit(f"Folder not found: {target_dir}")

    moved_count, skipped_count = organize_folder(target_dir, args.dry_run)

    mode = "Previewed" if args.dry_run else "Organized"
    print(f"\n{mode} {moved_count} file(s). Skipped {skipped_count} file(s).")


if __name__ == "__main__":
    main()
