import re
from enum import Enum
from htmlnode import LeafNode, HTMLNode, ParentNode
from textnode import TextNode, TextType
from functions import text_to_textnodes, text_node_to_html_node, split_nodes_delimiter


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(md: str) -> BlockType:
    match(md):
        case md if md.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return BlockType.HEADING
        case md if md.startswith("```"):
            return BlockType.CODE
        case md if md.startswith("> "):
            return BlockType.QUOTE
        case md if md.startswith("- "):
            return BlockType.UNORDERED_LIST
        case md if md.startswith("1. "):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH


def block_to_html(md: str, block_type: BlockType) -> HTMLNode:
    """Converts markdown block to html nodes"""
    match(block_type):
        case BlockType.HEADING:
            return heading_block_to_html(md)
        case BlockType.PARAGRAPH:
            return paragraph_block_to_html(md)
        case BlockType.QUOTE:
            return quote_block_to_html(md)
        case BlockType.UNORDERED_LIST:
            return list_block_to_html(md, BlockType.UNORDERED_LIST)
        case BlockType.ORDERED_LIST:
            return list_block_to_html(md, BlockType.ORDERED_LIST)
        case BlockType.CODE:
            return code_block_to_html(md)
        case _:
            return paragraph_block_to_html(md)


def text_to_children(md: str) -> list[HTMLNode]:
    """Converts a string to a list of HTMLNodes to be used as children for ParentNodes"""
    text_nodes = text_to_textnodes(md)
    new_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        new_nodes.append(html_node)
    return new_nodes


def code_block_to_html(md: str) -> list[HTMLNode]:
    formatted_lines = '\n'.join(
        [line for line in md.split("\n") if not line.startswith("```")])
    code_node = LeafNode("code", formatted_lines)
    return ParentNode("pre", [code_node])


def list_block_to_html(md: str, block_type: BlockType) -> list[HTMLNode]:
    """Convert list markdown block to html nodes"""
    md = md.replace("\n", "")
    if block_type == BlockType.ORDERED_LIST:
        md = re.sub(r"\d+\.", "- ", md)

    texts = md.split("- ")
    children = []
    for text in texts:
        html_nodes = text_to_children(text)
        if len(html_nodes) < 2:
            li_node = map(lambda node: LeafNode(
                "li", node.to_html()), html_nodes)
        else:
            html_nodes = [node.to_html() for node in html_nodes]
            li_text = ''.join(html_nodes)
            li_node = [LeafNode("li", li_text)]
        children.extend(li_node)

    if block_type == BlockType.ORDERED_LIST:
        return ParentNode("ol", children)
    else:
        return ParentNode("ul", children)


def quote_block_to_html(md: str) -> HTMLNode:
    """Convert quote markdown block to html nodes"""
    md = md.replace("> ", "")
    children = text_to_children(md)
    return ParentNode("blockquote", children)


def paragraph_block_to_html(md: str) -> HTMLNode:
    """Converts a pragraph block to HTMLNode"""
    # convert md to textnode
    md = md.replace("\n", " ")
    children = text_to_children(md)
    return ParentNode("p", children)


def heading_block_to_html(md: str) -> LeafNode:
    """
    Converts a heading block to html leaf node
    """
    hash_count = md.count("#")
    md = md.replace("#"*hash_count + " ", "")
    children = text_to_children(md)
    match(hash_count):
        case 1:
            return ParentNode("h1", children)
        case 2:
            return ParentNode("h2", children)
        case 3:
            return ParentNode("h3", children)
        case 4:
            return ParentNode("h4", children)
        case 5:
            return ParentNode("h5", children)
        case 6:
            return ParentNode("h6", children)
        case _:
            return ParentNode("p", children)
