import os
import shutil

working_directory = os.path.abspath(".")
dest_dir = os.path.join(working_directory, "public")
src_dir = os.path.join(working_directory, "static")


def copy_dir_to_public(src_path=src_dir, dest_path=dest_dir):
    # remove all the contents from public to ensure clean copy
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    # Create a new directory
    os.mkdir(dest_path)

    # copy contents
    items = os.listdir(src_path)
    for item in items:
        current_item_path = os.path.join(src_path, item)
        if os.path.isfile(current_item_path):
            shutil.copy(current_item_path, dest_path)
        else:
            new_dest_path = os.path.join(dest_path, item)
            os.mkdir(new_dest_path)
            copy_dir_to_public(current_item_path, new_dest_path)
