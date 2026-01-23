import re

from src.core.enums import BlockType
from src.core.htmlnode import HTMLNode, LeafNode, ParentNode
from src.parser.text_parser import text_node_to_html_node, text_to_textnodes


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Converts markdown blocks to a list of strings
    """
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    return list(filter(lambda x: x != "", blocks))


def block_to_block_type(md: str) -> BlockType:
    lines = md.split("\n")
    match md:
        case md if md.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return BlockType.HEADING
        case md if md.startswith("```"):
            return BlockType.CODE
        case md if md.startswith("> "):
            return BlockType.QUOTE
        case md if md.startswith(("- ", "* ", "+ ")):
            return BlockType.UNORDERED_LIST
        case md if md.startswith("1. "):
            return BlockType.ORDERED_LIST
        case md if (
            len(lines) > 1 and "|" in lines[0] and "|" in lines[1] and "-" in lines[1]
        ):
            return BlockType.TABLE
        case _:
            return BlockType.PARAGRAPH


def block_to_html(md: str, block_type: BlockType) -> HTMLNode:
    """Converts markdown block to html nodes"""
    match block_type:
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
        case BlockType.TABLE:
            return table_block_to_html(md)
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


def table_block_to_html(md: str) -> ParentNode:
    """Converts table markdown block to html table"""
    lines = md.split("\n")
    table_children = []

    # Header of table is the first line
    header_line = lines[0]
    # Get the title for the header by striping '|' first and then spliting on '|'
    headers = [h.strip() for h in header_line.strip("|").split("|")]
    header_cells = []
    for header in headers:
        header_node = text_to_children(header)
        th = ParentNode("th", header_node)
        header_cells.append(th)

    # Create header row
    header_row = ParentNode("tr", header_cells)
    table_children.append(header_row)

    for i in range(2, len(lines)):
        # Skip the first index as it only contains | --- | --- |
        row_line = lines[i]
        cells = [cell.strip() for cell in row_line.strip("|").split("|")]
        row_cells = []
        for cell in cells:
            cell_node = text_to_children(cell)
            td = ParentNode("td", cell_node)
            row_cells.append(td)

        data_row = ParentNode("tr", row_cells)
        table_children.append(data_row)

    return ParentNode("table", table_children)


def code_block_to_html(md: str) -> HTMLNode:
    """Return formatted code block in HTML"""
    formatted_lines = "\n".join(
        [line for line in md.split("\n") if not line.startswith("```")]
    )
    code_node = LeafNode("code", formatted_lines)
    return ParentNode("pre", [code_node])


def list_block_to_html(md: str, block_type: BlockType) -> HTMLNode:
    """Convert list markdown block to html nodes"""
    lines = md.split("\n")
    children = []
    for line in lines:
        text = ""
        if block_type == BlockType.ORDERED_LIST:
            text = re.sub(r"^\d+\. ", "", line)
        else:
            text = re.sub(r"^[-*+] ", "", line)

        html_nodes = text_to_children(text)
        li_node = LeafNode(
            "li", "".join(list(map(lambda node: node.to_html(), html_nodes)))
        )

        children.append(li_node)

    tag = "ol" if block_type == BlockType.ORDERED_LIST else "ul"
    return ParentNode(tag, children)


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


def heading_block_to_html(md: str) -> HTMLNode:
    """
    Converts a heading block to html leaf node
    """
    hash_count = md.count("#")
    md = md.replace("#" * hash_count + " ", "")
    children = text_to_children(md)
    match hash_count:
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
