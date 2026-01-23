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

    def copy_recursive(current_src, current_dest):
        items = os.listdir(current_src)
        for item in items:
            src_item_path = os.path.join(current_src, item)
            dest_item_path = os.path.join(current_dest, item)
            
            if os.path.isfile(src_item_path):
                shutil.copy(src_item_path, dest_item_path)
            else:
                os.mkdir(dest_item_path)
                copy_recursive(src_item_path, dest_item_path)

    copy_recursive(src_path, dest_path)
