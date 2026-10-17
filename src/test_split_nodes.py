import unittest
from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNode(unittest.TestCase):
    def test_delim_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is plain text", TextType.TEXT),
            ],
        )

    def test_delim_middle_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_start_bold(self):
        node = TextNode("**This is text** with a bold word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text", TextType.BOLD),
                TextNode(" with a bold word", TextType.TEXT),
            ],
        )

    def test_delim_end_italic(self):
        node = TextNode("This is text with a _italic word_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic word", TextType.ITALIC),
            ],
        )

    def test_delim_multiple_bold_sections(self):
        node = TextNode("This is **text** with **multiple bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with ", TextType.TEXT),
                TextNode("multiple bold", TextType.BOLD),
                TextNode(" words", TextType.TEXT),
            ],
        )

    def test_delim_multiple_input_nodes(self):
        node1 = TextNode("Hello, **world!**", TextType.TEXT)
        node2 = TextNode("Good **morning**, NYC", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Hello, ", TextType.TEXT),
                TextNode("world!", TextType.BOLD),
                TextNode("Good ", TextType.TEXT),
                TextNode("morning", TextType.BOLD),
                TextNode(", NYC", TextType.TEXT),
            ],
        )

    def test_delim_non_text_nodes(self):
        node1 = TextNode("non-text node", TextType.ITALIC)
        node2 = TextNode("total = a ** b", TextType.CODE)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("non-text node", TextType.ITALIC),
                TextNode("total = a ** b", TextType.CODE),
            ],
        )

    def test_delim_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [])

    def test_delim_entire_string_delimited(self):
        node = TextNode("`This entire string is a code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [TextNode("This entire string is a code block", TextType.CODE)],
        )

    def test_delim_multiple_calls(self):
        node = TextNode("This text has **adjacent**_delimiters_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This text has ", TextType.TEXT),
                TextNode("adjacent", TextType.BOLD),
                TextNode("delimiters", TextType.ITALIC),
            ],
        )

    def test_delim_unclosed_delimiter_raises(self):
        node = TextNode("Unclosed **bold delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
