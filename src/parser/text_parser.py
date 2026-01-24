import re

from src.core.enums import TextType
from src.core.htmlnode import LeafNode
from src.core.textnode import TextNode


def text_node_to_html_node(text_node) -> LeafNode:
    """
    Converts a TextNode to an HTMLNode specifically a LeafNode

    accepts:
        - text_node: A TextNode object

    return:
        - LeafNode with a tag, value and props
    """
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            # return a LeafNode with no tag, just raw text value
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            # return a LeafNode with b tag
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            # return a LeafNode with i tag
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            # return a LeafNode with code tag
            return LeafNode(tag="code", value=text_node.text)
        case TextType.STRIKETHROUGH:
            return LeafNode(tag="s", value=text_node.text)
        case TextType.LINKS:
            # return a LeafNode with a tag and href as props
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGES:
            # return a LeafNode iwth img tag and src, alt props
            url = text_node.url
            if url.lower().endswith((".png", ".jpg", ".jpeg")):
                base = url.split(".", 1)[0]
                url = f"{base}.webp"
            return LeafNode(
                tag="img", value="", props={"src": url, "alt": text_node.text, "loading": "lazy"}
            )
        case _:
            # raise exception on any other TextType
            raise Exception(f"{text_node} is not a valid TextNode!")


def split_nodes_delimiter(
    old_nodes: list[TextNode], dilimiter: str, text_type: TextType
) -> list:
    """
    Accepts a list of TextNodes extracts any inline nodes that might be presesnt using the passed dilimiter.

    accepts:
        - old nodes: a list of TextNodes
        - dilimiter: a string representing a dilimiter
        - text_type: TextType for the extraction

    return:
        - a list of TextNodes extracted from the old nodes
    """
    extracted_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            extracted_nodes.append(node)
            continue

        if node.text.count(dilimiter) % 2 != 0:
            raise Exception(
                f"Invalid Markdown Syntax! Matching {dilimiter} was not found in {
                    node.text
                }."
            )

        new_nodes = []
        split_strings = node.text.split(dilimiter)
        for i in range(len(split_strings)):
            if split_strings[i] == "":
                continue
            if i % 2 != 0:
                new_nodes.append(TextNode(split_strings[i], text_type))
            else:
                new_nodes.append(
                    TextNode(split_strings[i], TextType.PLAIN_TEXT))
        extracted_nodes.extend(new_nodes)

    return extracted_nodes


def extract_markdown_images(text) -> list:
    """
    Extracts the alt text and url from a markdown image link.

    accepts:
        - text: a string containing "![alt](url)"

    return:
        - a list of tuples -> [(alt, url)]
    """
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text) -> list:
    """
    Extracts the text and url from a markdown link.

    accepts:
        - text: a string containing "[text](url)"

    return:
        - a list of tuples -> [(text, url)]
    """
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):
    """
    Accepts a list of TextNodes extracts any inline nodes of markdown images that might be presesnt.

    accepts:
        - old nodes: a list of TextNodes

    return:
        - a list of TextNodes extracted from the old nodes
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for alt, url in images:
            sections = original_text.split(f"![{alt}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
            new_nodes.append(
                TextNode(
                    alt,
                    TextType.IMAGES,
                    url,
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    """
    Accepts a list of TextNodes extracts any inline nodes of markdown link that might be presesnt.

    accepts:
        - old nodes: a list of TextNodes

    return:
        - a list of TextNodes extracted from the old nodes
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for text, url in links:
            sections = original_text.split(f"[{text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))
            new_nodes.append(
                TextNode(
                    text,
                    TextType.LINKS,
                    url,
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Converts a simple markdown text string to a list of TextNodes
    """
    node = TextNode(text, TextType.PLAIN_TEXT)
    # Bold Nodes
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)
    # Italics Nodes
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    # Strikethrough
    nodes = split_nodes_delimiter(nodes, "~~", TextType.STRIKETHROUGH)
    # Code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    link_nodes = split_nodes_link(nodes)
    return split_nodes_image(link_nodes)


def extract_title(markdown: str) -> str:
    """Extract and return heading 1 from a md document"""
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.replace("# ", "").strip()
    raise Exception("No Heading found that starts with '#'.")
