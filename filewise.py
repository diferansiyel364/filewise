import hashlib
import os
import argparse


def calculate_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, OSError) as error:
        print(f"Cannot read {file_path}: {error}")
        return None


def find_duplicates(folder):
    """Find duplicate files inside a folder."""
    hashes = {}

    for root, _, files in os.walk(folder):
        for filename in files:
            path = os.path.join(root, filename)
            file_hash = calculate_hash(path)

            if file_hash:
                hashes.setdefault(file_hash, []).append(path)

    duplicates = [paths for paths in hashes.values() if len(paths) > 1]
    return duplicates


def main():
    parser = argparse.ArgumentParser(
        description="Find duplicate files using SHA-256."
    )
    parser.add_argument("folder", help="Folder to scan")
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print("Error: Folder does not exist.")
        return

    duplicates = find_duplicates(args.folder)

    if not duplicates:
        print("No duplicate files found.")
        return

    print("\nDuplicate files found:\n")

    for group in duplicates:
        print("\n".join(f"  - {path}" for path in group))
        print()

    print(f"Found {len(duplicates)} groups of duplicate files.")


if __name__ == "__main__":
    main()
