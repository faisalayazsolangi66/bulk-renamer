#!/usr/bin/env python3
"""Rename many files at once with a pattern, prefix, or numbering.

Usage:
    python3 main.py <folder> --prefix IMG_ --start 1
    python3 main.py <folder> --pattern "photo_{n:03d}" --extension .jpg
"""
import argparse
import re
from pathlib import Path


def build_name(pattern: str, index: int, original: Path) -> str:
    name = pattern
    name = name.replace("{n}", str(index))
    name = name.replace("{name}", original.stem)
    name = name.replace("{ext}", original.suffix.lstrip("."))
    # Support {n:03d} style zero-padded numbering.
    def _pad(match):
        width = int(match.group(1))
        return str(index).zfill(width)
    name = re.sub(r"\{n:0(\d+)d\}", _pad, name)
    return name


def rename_files(folder: Path, pattern: str, prefix: str, suffix: str,
                 start: int, extension: str, dry_run: bool, recursive: bool):
    glob = folder.rglob("*") if recursive else folder.iterdir()
    files = sorted(p for p in glob if p.is_file())
    if extension:
        ext = extension if extension.startswith(".") else f".{extension}"
        files = [p for p in files if p.suffix.lower() == ext.lower()]
    if not files:
        print("No matching files found.")
        return
    for i, src in enumerate(files, start=start):
        if pattern:
            new_stem = build_name(pattern, i, src)
            new_name = new_stem if "." in new_stem else new_stem + src.suffix
        else:
            new_name = f"{prefix}{src.stem}{suffix}{src.suffix}"
        dest = src.with_name(new_name)
        if dest == src:
            print(f"Skipping (unchanged): {src.name}")
            continue
        if dest.exists():
            print(f"Skipping (target exists): {src.name} -> {new_name}")
            continue
        if dry_run:
            print(f"[dry-run] {src.name} -> {new_name}")
        else:
            src.rename(dest)
            print(f"{src.name} -> {new_name}")
    print(f"Done. {len(files)} file(s) considered.")


def main():
    parser = argparse.ArgumentParser(
        description="Rename many files at once with a pattern, prefix, or numbering.")
    parser.add_argument("folder", type=Path, help="Folder containing the files")
    parser.add_argument("--pattern", default="",
                        help='Naming pattern, e.g. "photo_{n:03d}" or "{name}_v2". '
                             "Supports {n}, {n:03d}, {name}, {ext}.")
    parser.add_argument("--prefix", default="", help="Text to prepend to each name")
    parser.add_argument("--suffix", default="", help="Text to append to each stem")
    parser.add_argument("--start", type=int, default=1,
                        help="Starting number for {n} (default: 1)")
    parser.add_argument("--extension", default="",
                        help="Only rename files with this extension, e.g. .jpg")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show planned renames without renaming anything")
    parser.add_argument("--recursive", action="store_true",
                        help="Also rename files in subfolders")
    args = parser.parse_args()
    if not args.folder.is_dir():
        parser.error(f"not a directory: {args.folder}")
    if not args.pattern and not args.prefix and not args.suffix:
        parser.error("give --pattern, --prefix, or --suffix")
    rename_files(args.folder, args.pattern, args.prefix, args.suffix,
                 args.start, args.extension, args.dry_run, args.recursive)


if __name__ == "__main__":
    main()
