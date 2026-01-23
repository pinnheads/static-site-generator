import unittest
from src.core.enums import BlockType
from src.parser.block_parser import block_to_block_type, table_block_to_html


class TestTableMarkdown(unittest.TestCase):
    def test_block_type_table(self):
        md = """| Header 1 | Header 2 |
| --- | --- |
| Cell 1 | Cell 2 |"""
        self.assertEqual(block_to_block_type(md), BlockType.TABLE)

    def test_table_conversion(self):
        md = """| Name | Age |
| --- | --- |
| Alice | 30 |
| Bob | 25 |"""
        node = table_block_to_html(md)
        html = node.to_html()
        
        # Verify structure
        self.assertTrue(html.startswith("<table>"))
        self.assertTrue(html.endswith("</table>"))
        
        # Verify headers
        self.assertIn("<tr><th>Name</th><th>Age</th></tr>", html)
        
        # Verify data rows
        self.assertIn("<tr><td>Alice</td><td>30</td></tr>", html)
        self.assertIn("<tr><td>Bob</td><td>25</td></tr>", html)

    def test_table_with_inline_markdown(self):
        md = """| **Bold** | *Italic* |
| --- | --- |
| `Code` | [Link](url) |"""
        node = table_block_to_html(md)
        html = node.to_html()
        
        self.assertIn("<th><b>Bold</b></th>", html)
        self.assertIn("<th><i>Italic</i></th>", html)
        self.assertIn("<td><code>Code</code></td>", html)
        self.assertIn('<td><a href="url">Link</a></td>', html)

if __name__ == "__main__":
    unittest.main()
