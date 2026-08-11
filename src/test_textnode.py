import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    # --- Equality & inequality basics ---
    def test_equality_same_values(self):
        a = TextNode("hello", TextType.TEXT)
        b = TextNode("hello", TextType.TEXT)
        self.assertEqual(a, b)

    def test_inequality_different_text(self):
        a = TextNode("hello", TextType.TEXT)
        b = TextNode("world", TextType.TEXT)
        self.assertNotEqual(a, b)

    def test_inequality_different_type(self):
        a = TextNode("hello", TextType.TEXT)
        b = TextNode("hello", TextType.BOLD)
        self.assertNotEqual(a, b)

    def test_inequality_different_url(self):
        a = TextNode("click", TextType.LINK, "https://a.example")
        b = TextNode("click", TextType.LINK, "https://b.example")
        self.assertNotEqual(a, b)

    # --- URL handling for LINK/IMAGE vs none ---
    def test_link_without_url_defaults_none(self):
        n = TextNode("click me", TextType.LINK)
        self.assertIsNone(n.url)

    def test_image_with_url(self):
        n = TextNode("alt text", TextType.IMAGE, "https://img.example/cat.png")
        self.assertEqual(n.url, "https://img.example/cat.png")

    # --- __repr__ format ---
    def test_repr_without_url(self):
        n = TextNode("hello", TextType.TEXT)
        self.assertEqual(repr(n), "TextNode(hello, TextType.TEXT, None)")

    def test_repr_with_url(self):
        n = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(repr(n), "TextNode(Boot.dev, TextType.LINK, https://www.boot.dev)")

    # --- Equality properties ---
    def test_equality_transitive(self):
        a = TextNode("x", TextType.CODE)
        b = TextNode("x", TextType.CODE)
        c = TextNode("x", TextType.CODE)
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertEqual(a, c)  # transitivity

    def test_equality_symmetric(self):
        a = TextNode("x", TextType.ITALIC, None)
        b = TextNode("x", TextType.ITALIC, None)
        self.assertTrue(a == b and b == a)

    # --- Enum sanity ---
    def test_enum_values_exist(self):
        self.assertEqual(TextType.TEXT.value, "text")
        self.assertEqual(TextType.BOLD.value, "bold")
        self.assertEqual(TextType.ITALIC.value, "italic")
        self.assertEqual(TextType.CODE.value, "code")
        self.assertEqual(TextType.LINK.value, "link")
        self.assertEqual(TextType.IMAGE.value, "image")

    # --- Mutability impact on equality ---
    def test_mutation_changes_equality(self):
        a = TextNode("same", TextType.TEXT)
        b = TextNode("same", TextType.TEXT)
        self.assertEqual(a, b)
        a.text = "different"
        self.assertNotEqual(a, b)

    # --- Behavior with non-TextNode (documenting current behavior) ---
    def test_eq_with_non_textnode_raises_attributeerror(self):
        a = TextNode("x", TextType.TEXT)
        with self.assertRaises(AttributeError):
            _ = (a == "not a TextNode")  # current __eq__ assumes same attributes


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold!", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold!")
        self.assertIsNone(html_node.props)

    def test_italic(self):
        node = TextNode("italics", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italics")

    def test_code(self):
        node = TextNode("x = 1", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "x = 1")

    def test_link_with_url(self):
        node = TextNode("Click me", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_link_without_url(self):
        node = TextNode("Click me", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        # main creates {"href": text_node.url} so expect None when url omitted
        self.assertEqual(html_node.props, {"href": None})

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://img.example/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        # main maps image value to empty string
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://img.example/cat.png", "alt": "alt text"})

    def test_invalid_text_type_raises(self):
        node = TextNode("x", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)



if __name__ == "__main__":
    unittest.main()