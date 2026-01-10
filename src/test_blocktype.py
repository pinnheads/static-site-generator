import unittest

from blocktype import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):
    def test_headings(self):
        headings = ["# This is a heading1", "## This is heading2", "### This is heading3",
                    "#### This is heading4", "##### This is heading5", "###### This is heading6"]
        for heading in headings:
            block_type = block_to_block_type(heading)
            self.assertEqual(block_type, BlockType.HEADING)

    def test_code(self):
        code = """```python
            print('hello world!')
        ```
        """
        block_type = block_to_block_type(code)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote(self):
        quote = "> This is a quote"
        block_type = block_to_block_type(quote)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_unordered_list(self):
        unordered_list = """- item 1
        - item 2
        - item 3
        - item 4
        """
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_not_unordered_list(self):
        unordered_list = """* item 1
        * item 2
        * item 3
        * item 4
        """
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        ordered_list = """1. Item 1
        2. Item 2
        3. Item 3
        4. Item 4
        """
        block_type = block_to_block_type(ordered_list)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_not_ordered_list(self):
        ordered_list = """1 Item 1
        2 Item 2
        3 Item 3
        4 Item 4
        """
        block_type = block_to_block_type(ordered_list)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraph(self):
        paragraph = "This is a normal paragraph"
        block_type = block_to_block_type(paragraph)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
