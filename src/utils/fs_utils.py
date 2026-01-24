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
                filename, ext = os.path.splitext(item)
                if ext.lower() in [".png", ".jpg", ".png"]:
                    try:
                        from PIL import Image
                        new_dest_path = os.path.join(
                            current_dest, f"{filename}.webp")
                        print(f"Converting: {item} -> {filename}.webp")

                        with Image.open(src_item_path) as img:
                            img.save(new_dest_path, "WEBP",
                                     quality=80, method=6)
                        continue
                    except ImportError:
                        print("Error in Importing PIL")
                        pass
                else:
                    shutil.copy(src_item_path, dest_item_path)
            else:
                os.mkdir(dest_item_path)
                copy_recursive(src_item_path, dest_item_path)

    copy_recursive(src_path, dest_path)
