import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()