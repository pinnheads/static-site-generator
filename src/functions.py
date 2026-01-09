from textnode import TextType, TextNode
from htmlnode import LeafNode


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
        case TextType.LINKS:
            # return a LeafNode with a tag and href as props
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGES:
            # return a LeafNode iwth img tag and src, alt props
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            # raise exception on any other TextType
            raise Exception(f"{text_node} is not a valid TextNode!")


def split_nodes_delimiter(old_nodes: list[TextNode], dilimiter: str, text_type: TextType) -> list:
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
            raise Exception(f"Invalid Markdown Syntax! Matching {
                            dilimiter} was not found in {node.text}.")

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
