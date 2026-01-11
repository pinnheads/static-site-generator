from htmlnode import HTMLNode, ParentNode
from functions import markdown_to_blocks
from blocktype import block_to_block_type, block_to_html


def markdown_to_html_node(markdown: str) -> HTMLNode:
    # split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    # loop over each block
    for block in blocks:
        # determine the type of block
        block_type = block_to_block_type(block)
        # based on each type of block create a new HTMLNode with proper data
        # assign the proper child HTMLNode objects to the block node
        child_nodes.append(block_to_html(block, block_type))
    # make all the block nodes children under a single parent HTMLNode
    return ParentNode("div", child_nodes)
