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
    print(os.makedirs(os.path.dirname(os.path.join(
        os.path.abspath("."), dest_path)), exist_ok=True))

    with open(dest_path, "w") as dest_file:
        dest_file.write(content)


def main():
    copy_dir_to_public()
    generate_page(from_path="content/index.md",
                  template_path="template.html", dest_path="public/index.html")
    generate_page(from_path="content/blog/glorfindel/index.md",
                  template_path="template.html", dest_path="public/blog/glorfindel/index.html")
    generate_page(from_path="content/blog/majesty/index.md",
                  template_path="template.html", dest_path="public/blog/majesty/index.html")
    generate_page(from_path="content/blog/tom/index.md",
                  template_path="template.html", dest_path="public/blog/tom/index.html")
    generate_page(from_path="content/contact/index.md",
                  template_path="template.html", dest_path="public/contact/index.html")


if __name__ == "__main__":
    main()
