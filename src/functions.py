from textnode import TextType
from htmlnode import LeafNode


def text_node_to_html_node(text_node) -> LeafNode:
    """
    Converts a TextNode to an HTMLNode specifically a LeafNode

    Accepts:
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
