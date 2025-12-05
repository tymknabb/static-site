import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    
    def test_init(self):
        node = HTMLNode("a", "hello world", None, {"href":"https://google.com"})
        self.assertIsInstance(node, HTMLNode)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "hello world")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href":"https://google.com"})

    def test_to_html(self):
        node = HTMLNode("p", "hello world", None, None)
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("a", "hello world", None, {"href":"https://mail.google.com", "target":"_blank"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://mail.google.com" target="_blank"')


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")


class TestParentNode(unittest.TestCase):

    def test_to_html_no_tag(self):
        child_node = LeafNode("p", "Nothing to see here")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()    

    def test_to_html_no_children(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child_node_1 = LeafNode("b", "Bold text")
        child_node_2 = LeafNode(None, "Normal text")
        child_node_3 = LeafNode("i", "Italic text")
        child_node_4 = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child_node_1, child_node_2, child_node_3, child_node_4])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()