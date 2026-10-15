import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_default_values(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html_empty_or_none(self):
        node_none = HTMLNode()
        node_empty = HTMLNode(props={})
        self.assertEqual(node_none.props_to_html(), "")
        self.assertEqual(node_empty.props_to_html(), "")

    def test_prop_to_html_one_attribute(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_prop_to_html_multiple_attributes(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode("img", "alt text", {"src": "image.png", "width": "500"})
        self.assertEqual(node.to_html(), '<img src="image.png" width="500">alt text</img>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("b", "Bold text")
        child_node2 = LeafNode(None, "Normal text")
        child_node3 = LeafNode("i", "italic text")
        child_node4 = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child_node1, child_node2, child_node3, child_node4])

        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_to_html_with_great_grandchildren(self):
        great_grandchild_node = LeafNode("i", "great_grandchild")
        grandchild_node = ParentNode("b", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><i>great_grandchild</i></b></span></div>",
        )

    def test_to_html_with_no_children(self):
        node1 = ParentNode("div", None)
        node2 = ParentNode("div", [])

        with self.assertRaises(ValueError):
            node1.to_html()
        with self.assertRaises(ValueError):
            node2.to_html()

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "menu"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="menu"><span>child</span></div>',
        )

    def test_to_html_with_no_nested_tag(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode(None, [grandchild_node])
        parent_node = ParentNode("p", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()
