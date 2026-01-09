import unittest
from functions import extract_markdown_images, extract_markdown_links


class TestExtractionMarkdownImagesAndLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_alt(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [Utsav Deep](https://utsavdeep.com)"
        )
        self.assertListEqual(
            [("Utsav Deep", "https://utsavdeep.com")], matches)

    def test_extract_markdown_links_no_text(self):
        matches = extract_markdown_links(
            "This is text with an [](https://utsavdeep.com)"
        )
        self.assertListEqual(
            [("", "https://utsavdeep.com")], matches)

    def test_extract_markdown_images_with_link(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://example.com)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_with_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://example.com)"
        )
        self.assertListEqual(
            [("link", "https://example.com")], matches)


if __name__ == "__main__":
    unittest.main()
