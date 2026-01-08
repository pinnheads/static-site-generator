import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    # Check HTMLNode class
    def test_check_props(self):
        node = HTMLNode("a", "Utsav Deep", [], {
                        "href": "https://utsavdeep.com", "target": "_blank"})
        self.assertIn("href", node.props_to_html())
        self.assertIn("target", node.props_to_html())

    def test_props_none(self):
        node = HTMLNode("p", "Lorem Ipsum")
        self.assertTrue('' == node.props_to_html())

    def test_HTMLNode(self):
        node = HTMLNode("span", value=None, children=[
                        '<p>HTML Node is working?</p>'], props={"style": "color: blue;"})
        self.assertTrue("HTMLNode" in repr(node))

    # Check LeafNode Class
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_error(self):
        node = LeafNode("a", value=None, props={
                        "href": "https://utsavdeep.com"})
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual("Hello, world!", node.to_html())


if __name__ == "__main__":
    unittest.main()
