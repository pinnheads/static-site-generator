import unittest
from src.core.enums import TextType
from src.core.textnode import TextNode
from src.parser.text_parser import text_node_to_html_node, text_to_textnodes


class TestStrikethrough(unittest.TestCase):
    def test_text_node_to_html_node_strikethrough(self):
        node = TextNode("This is strikethrough", TextType.STRIKETHROUGH)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "s")
        self.assertEqual(html_node.value, "This is strikethrough")
        self.assertEqual(html_node.to_html(), "<s>This is strikethrough</s>")

    def test_text_to_textnodes_strikethrough(self):
        text = "This is ~~strikethrough~~ text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.PLAIN_TEXT)
        self.assertEqual(nodes[1].text, "strikethrough")
        self.assertEqual(nodes[1].text_type, TextType.STRIKETHROUGH)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.PLAIN_TEXT)

    def test_text_to_textnodes_mixed(self):
        text = "This is **bold** and ~~strikethrough~~"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 4)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[3].text, "strikethrough")
        self.assertEqual(nodes[3].text_type, TextType.STRIKETHROUGH)

if __name__ == "__main__":
    unittest.main()
