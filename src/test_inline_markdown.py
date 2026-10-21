import unittest
from inline_markdown import *
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delim_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is plain text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_middle_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_start_bold(self):
        node = TextNode("**This is text** with a bold word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text", TextType.BOLD),
                TextNode(" with a bold word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_end_italic(self):
        node = TextNode("This is text with a _italic word_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic word", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_multiple_bold_sections(self):
        node = TextNode("This is **text** with **multiple bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with ", TextType.TEXT),
                TextNode("multiple bold", TextType.BOLD),
                TextNode(" words", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_multiple_input_nodes(self):
        node1 = TextNode("Hello, **world!**", TextType.TEXT)
        node2 = TextNode("Good **morning**, NYC", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Hello, ", TextType.TEXT),
                TextNode("world!", TextType.BOLD),
                TextNode("Good ", TextType.TEXT),
                TextNode("morning", TextType.BOLD),
                TextNode(", NYC", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_non_text_nodes(self):
        node1 = TextNode("non-text node", TextType.ITALIC)
        node2 = TextNode("total = a ** b", TextType.CODE)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("non-text node", TextType.ITALIC),
                TextNode("total = a ** b", TextType.CODE),
            ],
            new_nodes,
        )

    def test_delim_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([], new_nodes)

    def test_delim_empty_string_non_text(self):
        node = TextNode("", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([], new_nodes)

    def test_delim_entire_string_delimited(self):
        node = TextNode("`This entire string is a code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [TextNode("This entire string is a code block", TextType.CODE)],
            new_nodes,
        )

    def test_delim_multiple_calls(self):
        node = TextNode("This text has **adjacent**_delimiters_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.TEXT),
                TextNode("adjacent", TextType.BOLD),
                TextNode("delimiters", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_unclosed_delimiter_raises(self):
        node = TextNode("Unclosed **bold delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestSplitNodesImages(unittest.TestCase):
    def test_no_images(self):
        node = TextNode("This has no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This has no images", TextType.TEXT)],
            new_nodes,
        )

    def test_image_in_middle(self):
        node = TextNode("This has a ![image](https://i.imgur.com/zjjcJKZ.png) in the middle", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This has a ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" in the middle", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) at the start", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the start", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_image_at_end(self):
        node = TextNode("This has a image at the end ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This has a image at the end ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_multiple_images(self):
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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_image_with_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and an [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and an [link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_multiple_input_nodes(self):
        node1 = TextNode("First ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node2 = TextNode("![second image](https://i.imgur.com/3elNhQu.png) after that", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" after that", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_entire_string(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_image_non_text_nodes(self):
        node1 = TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        node2 = TextNode("another image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("another image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_image_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([], new_nodes)



class TestSplitNodesLinks(unittest.TestCase):
    def test_no_links(self):
        node = TextNode("This has no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This has no links", TextType.TEXT)],
            new_nodes,
        )

    def test_link_in_middle(self):
        node = TextNode("This has a [link](https://www.boot.dev) in the middle", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" in the middle", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_start(self):
        node = TextNode("[link](https://www.boot.dev) at the start", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" at the start", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_link_at_end(self):
        node = TextNode("This has a link at the end [link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has a link at the end ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with an [link](https://www.boot.dev) and another [second link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_link_with_image(self):
        node = TextNode(
            "This is text with an [link](https://www.boot.dev) and an ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and an ![image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_multiple_input_nodes(self):
        node1 = TextNode("First [link](https://www.boot.dev)", TextType.TEXT)
        node2 = TextNode("[second link](https://www.google.com) after that", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode("second link", TextType.LINK, "https://www.google.com"),
                TextNode(" after that", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_entire_string(self):
        node = TextNode("[link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_link_non_text_nodes(self):
        node1 = TextNode("link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("another link", TextType.LINK, "https://www.google.com")
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode("another link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

    def test_link_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([], new_nodes)


class TestSplitNodesImagesLinks(unittest.TestCase):
    def test_image_link_multiple_calls(self):
        node = TextNode(
            "First [link](https://www.boot.dev) followed by an ![image](https://i.imgur.com/zjjcJKZ.png) and a [second link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" followed by an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes
        )

if __name__ == "__main__":
    unittest.main()
