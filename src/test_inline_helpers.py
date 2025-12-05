import unittest

from textnode import TextNode, TextType
from inline_helpers import *


class TestInlineHelpers(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_a_href(self):
        node = TextNode("This is a link", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_img_src_alt(self):
        node = TextNode("This is alt text", TextType.IMAGE, "banana.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "banana.jpg", "alt": "This is alt text"})

    def test_split_md_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        print(type(new_nodes))
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type.value, "bold")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type.value, "text")

    def test_split_md_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type.value, "italic")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type.value, "text")

    def test_split_md_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type.value, "code")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type.value, "text")

    def test_split_invalid_md(self):
        node = TextNode("This is text with a `code block` word. Also this is wrong`", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://google.com)"
        )
        self.assertListEqual([("link", "https://google.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://google.com) and another [second link](https://duckduckgo.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://duckduckgo.com"
                ),
            ],
            new_nodes,
        )

    def test_text_to_nodes_single(self):
        md = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://google.com)"
        new_nodes = text_to_textnodes(md)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

    def test_text_to_nodes_multiple(self):
        md = "This is **text** with an _italic_ **word** and a `code block` _and_ an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) `and` a [link](https://google.com)"
        new_nodes = text_to_textnodes(md)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT), 
                TextNode("text", TextType.BOLD), 
                TextNode(" with an ", TextType.TEXT), 
                TextNode("italic", TextType.ITALIC), 
                TextNode(" ", TextType.TEXT), 
                TextNode("word", TextType.BOLD), 
                TextNode(" and a ", TextType.TEXT), 
                TextNode("code block", TextType.CODE), 
                TextNode(" ", TextType.TEXT), 
                TextNode("and", TextType.ITALIC), 
                TextNode(" an ", TextType.TEXT), 
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                TextNode(" ", TextType.TEXT), 
                TextNode("and", TextType.CODE), 
                TextNode(" a ", TextType.TEXT), 
                TextNode("link", TextType.LINK, "https://google.com")
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()