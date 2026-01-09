import unittest

from textnode import TextNode, TextType
from functions import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a image node",
                        TextType.IMAGES, "https://example.com")
        node2 = TextNode("This is another image node",
                         TextType.IMAGES, "https://utsavdeep.com")
        self.assertNotEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is plain text", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a link", TextType.LINKS,
                         "https://utsavdeep.com")
        self.assertNotEqual(node, node2)

    def test_text_to_leaf_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_leaf_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_text_to_leaf_italics(self):
        node = TextNode("This is a italics text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italics text node")

    def test_text_to_leaf_code(self):
        node = TextNode("print('hello world!')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello world!')")

    def test_text_to_leaf_links(self):
        node = TextNode("Utsav Deep", TextType.LINKS, "https://utsavdeep.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Utsav Deep")
        self.assertEqual(html_node.props["href"], "https://utsavdeep.com")

    def test_text_to_leaf_img(self):
        node = TextNode("example image", TextType.IMAGES,
                        "https://picsum.photos/200")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], node.url)
        self.assertEqual(html_node.props["alt"], node.text)

    def test_text_to_leaf_err(self):
        node = TextNode("example node", None, "bad url")
        self.assertRaises(Exception, text_node_to_html_node, node)


if __name__ == "__main__":
    unittest.main()
