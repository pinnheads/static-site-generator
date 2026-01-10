from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(md: str) -> BlockType:
    match(md):
        case md if md.startswith(("#", "##", "###", "####", "#####", "######")):
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
