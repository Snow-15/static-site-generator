import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a old node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a new node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.LINKS)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, None)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://google.com")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://bootdev.com")
        self.assertNotEqual(node, node2)

    def test_eq_url_text_none(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, None)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, "None")
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type_url(self):
        node = TextNode("This is a old node", TextType.BOLD_TEXT, "https://google.com")
        node2 = TextNode("This is a new node", TextType.ITALIC_TEXT, "https://bootdev.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
