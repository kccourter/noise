#!/usr/bin/env python3
"""
Copy a random sample of thermal imagery files from FLIR ADAS dataset.
"""

import os
import random
import re
import shutil
from pathlib import Path


def main():
    # Define paths
    SRC_FOLDER = Path.home() / "data" / "FLIR_ADAS_v2" / "images_thermal_train" / "data"
    DST_FOLDER = Path.home() / "data" / "noise" / "thermal" / "original"

    # Read filenames from source folder
    if not SRC_FOLDER.exists():
        print(f"ERROR: Source folder does not exist: {SRC_FOLDER}")
        return

    src_file_list = [f.name for f in SRC_FOLDER.iterdir() if f.is_file()]

    if len(src_file_list) == 0:
        print(f"ERROR: No files found in {SRC_FOLDER}")
        return

    print(f"Found {len(src_file_list)} files in source folder")

    # Ask user for number of files to copy
    num_files = int(input("How many files would you like to copy? "))

    # Seed random number generator for reproducibility
    random.seed(42)

    # Create random index list
    num_samples = min(num_files, len(src_file_list))
    index_list = random.sample(range(len(src_file_list)), num_samples)

    # Create destination folder
    DST_FOLDER.mkdir(parents=True, exist_ok=True)

    # Create src_file_list.txt
    list_file_path = DST_FOLDER / "src_file_list.txt"

    with open(list_file_path, 'w') as list_file:
        for idx in index_list:
            src_filename = src_file_list[idx]
            list_file.write(f"{src_filename}\n")

            # Extract the frame number portion (fname_000nnn pattern)
            # The FLIR ADAS files have names like: video-XXX-frame-000591-YYY.jpg
            # Extract just the "frame-000591" portion
            match = re.search(r'frame-\d{6}', src_filename)
            if match:
                dst_file_name = f"{match.group()}.jpg"
            else:
                # Fallback to full base name if pattern not found
                dst_file_name = f"{Path(src_filename).stem}.jpg"

            src_path = SRC_FOLDER / src_filename
            dst_path = DST_FOLDER / dst_file_name

            print(f"copying {src_filename} to ./data/{dst_file_name}")

            # Copy the file
            shutil.copy2(src_path, dst_path)

    print(f"\nCompleted! Copied {num_samples} files to {DST_FOLDER}")
    print(f"Source file list saved to {list_file_path}")


if __name__ == "__main__":
    main()
