import unittest

from block_helpers import *


class TestBlockHelpers(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empties(self):
        md = """
This is **bolded** paragraph

  

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

    

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.U_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.O_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# This is a heading in an h1 tag

## This is a heading in an h2 tag

### This is a heading in an h3 tag

#### This is a heading in an h4 tag

##### This is a heading in an h5 tag

###### This is a heading in an h6 tag
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading in an h1 tag</h1><h2>This is a heading in an h2 tag</h2><h3>This is a heading in an h3 tag</h3><h4>This is a heading in an h4 tag</h4><h5>This is a heading in an h5 tag</h5><h6>This is a heading in an h6 tag</h6></div>",
        )

    def test_ordered_list(self):
        md = """
1. Item number 1
2. Item number 2
3. Item number 3

4. Just a paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item number 1</li><li>Item number 2</li><li>Item number 3</li></ol><p>4. Just a paragraph</p></div>",
        )

    def test_unordered_list(self):
        md = """
- Item
- Another item
- Well, it's an item

-this is a paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item</li><li>Another item</li><li>Well, it's an item</li></ul><p>-this is a paragraph</p></div>",
        )

    def test_quote_block(self):
        md = """
>Implying
>Further implying
>Literally projecting

Who are you quoting?
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Implying Further implying Literally projecting</blockquote><p>Who are you quoting?</p></div>",
        )


if __name__ == "__main__":
    unittest.main()