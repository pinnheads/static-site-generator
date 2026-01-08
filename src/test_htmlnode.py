import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
