from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = "plain_text"
    BOLD = "**bold_text**"
    ITALIC = "__italic_text__"
    CODE = "`code text`"
    STRIKETHROUGH = "~~text~~"
    LINKS = "link: [anchor text](url)"
    IMAGES = "image: ![alt text](url)"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    TABLE = "table"
