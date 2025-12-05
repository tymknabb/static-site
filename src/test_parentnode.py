import unittest

from htmlnode import ParentNode, LeafNode


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