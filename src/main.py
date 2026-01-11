import os

from functions import extract_title
from markdowntohtml import markdown_to_html_node
from copytopublic import copy_dir_to_public


def generate_page(from_path: os.PathLike, template_path: os.PathLike, dest_path: os.PathLike):
    md_content = None
    template_content = None
    html_content = None

    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}")

    with open(from_path, "r") as src_file:
        md_content = src_file.read()

    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    html_content = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)

    content = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content)
    os.makedirs(os.path.dirname(os.path.join(
        os.path.abspath("."), dest_path)), exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(content)


def generate_page_recursive(dir_path_content="content/", template_path="template.html", dest_dir_path="public/"):
    # get abs paths
    src_path = os.path.join(os.path.abspath("."), dir_path_content)
    template = os.path.join(os.path.abspath("."), template_path)
    dest_dir = os.path.join(os.path.abspath("."), dest_dir_path)
    # copy contents
    items = os.listdir(src_path)
    for item in items:
        current_item_path = os.path.join(src_path, item)
        if os.path.isfile(current_item_path):
            generate_page(current_item_path, template,
                          os.path.join(dest_dir_path, item.replace(".md", ".html")))
        else:
            new_dest_path = os.path.join(dest_dir, item)
            generate_page_recursive(
                current_item_path, template_path, new_dest_path)


def main():
    copy_dir_to_public()
    generate_page_recursive()


if __name__ == "__main__":
    main()
