import unittest

from src.core.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # Check HTMLNode class
    def test_check_props(self):
        node = HTMLNode(
            "a", "Utsav Deep", [], {"href": "https://utsavdeep.com", "target": "_blank"}
        )
        self.assertIn("href", node.props_to_html())
        self.assertIn("target", node.props_to_html())

    def test_props_none(self):
        node = HTMLNode("p", "Lorem Ipsum")
        self.assertTrue("" == node.props_to_html())

    def test_HTMLNode(self):
        node = HTMLNode(
            "span",
            value=None,
            children=["<p>HTML Node is working?</p>"],
            props={"style": "color: blue;"},
        )
        self.assertTrue("HTMLNode" in repr(node))

    # Check LeafNode Class
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_error(self):
        node = LeafNode("a", value=None, props={"href": "https://utsavdeep.com"})
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual("Hello, world!", node.to_html())

    # Check Parent Node
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "Bold")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()
