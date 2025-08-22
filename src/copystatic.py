import os
import shutil


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):   # Create destination if it doesn't exist
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):    # Iterate through source directory
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")   # Log file operations
        if os.path.isfile(from_path):   # If it's a file, copy it
            shutil.copy(from_path, dest_path)
        else:   # If it's a directory, recurse
            copy_files_recursive(from_path, dest_path)
