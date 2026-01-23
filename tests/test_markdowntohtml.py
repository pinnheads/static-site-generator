import unittest
from src.parser.markdown_parser import markdown_to_html_node


class TestMarkDownToHTML(unittest.TestCase):
    def test_headings(self):
        md = """
# Heading 1 with `code`

## Heading 2 with **bold text**

### Heading 3 with _italic text_

#### Heading 4

##### Headning 5

###### Heading 6

"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><h1>Heading 1 with <code>code</code></h1><h2>Heading 2 with <b>bold text</b></h2><h3>Heading 3 with <i>italic text</i></h3><h4>Heading 4</h4><h5>Headning 5</h5><h6>Heading 6</h6></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_quotes(self):
        md = """
> We suffer more **often in imagination**,
> than in reality
> --- Seneca
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><blockquote>We suffer more <b>often in imagination</b>,\nthan in reality\n--- Seneca</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- This is item 1
- This is **bold item 2**

# Heading 1

1. This is _list 1_
2. This is `list 2`

> This is a test
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><ul><li>This is item 1</li><li>This is <b>bold item 2</b></li></ul><h1>Heading 1</h1><ol><li>This is <i>list 1</i></li><li>This is <code>list 2</code></li></ol><blockquote>This is a test</blockquote></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
