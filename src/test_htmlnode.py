import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        # Tests conversion of HTML attributes to proper string format
        node = HTMLNode(
            "a",
            "Visit our website",
            None,
            {"href": "https://www.example.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.example.com" target="_blank"',
        )

    def test_values(self):
        # Tests basic node initialization with just tag and value
        node = HTMLNode(
            "h1",
            "Welcome to our platform",
        )
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Welcome to our platform")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        """Test the debug string representation matches class implementation"""
        node = HTMLNode(
            "div",
            "Main content section",
            None,
            {"class": "container", "id": "main-content"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=div, value=Main content section, children=None, props={'class': 'container', 'id': 'main-content'})",
        )

    def test_leaf_to_html_p(self):
        # Tests LeafNode HTML rendering (paragraph)
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        # Tests LeafNode HTML rendering (anchor with attributes)
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>',)

    def test_leaf_to_html_no_tag(self):
        # Tests LeafNode raw text rendering (no tag)
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()