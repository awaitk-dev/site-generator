import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    child1 = HTMLNode('h1', 'child1text', None, {"href": "https://www.google.com"})
    child2 = HTMLNode('a', 'child2text', None, {"href": "https://www.boot.dev"})
    children = [child1, child2]
    
    def test_eq(self):
        node1 = HTMLNode('p', 'valuetext', TestHTMLNode.children, {"href": "https://www.yahoo.com"})
        node2 = HTMLNode('p', 'valuetext', TestHTMLNode.children, {"href": "https://www.yahoo.com"})
        self.assertEqual(node1, node2)
    
    def test_inequality_different_tag(self):
        a = HTMLNode('h1', '1text', TestHTMLNode.children, {"href": "https://www.google.com"})
        b = HTMLNode('a', '1text', TestHTMLNode.children, {"href": "https://www.google.com"})
        self.assertNotEqual(a, b)

    def test_inequality_different_text(self):
        a = HTMLNode('h1', '1text', TestHTMLNode.children, {"href": "https://www.google.com"})
        b = HTMLNode('h1', '2text', TestHTMLNode.children, {"href": "https://www.google.com"})
        self.assertNotEqual(a, b)
    
    def test_inequality_different_children(self):
        new_kids = [TestHTMLNode.child1, TestHTMLNode.child1, TestHTMLNode.child2]
        a = HTMLNode('h1', '1text', TestHTMLNode.children, {"href": "https://www.google.com"})
        b = HTMLNode('h1', '1text', new_kids, {"href": "https://www.google.com"})
        self.assertNotEqual(a, b)

    def test_inequality_different_props(self):
        a = HTMLNode('h1', '1text', TestHTMLNode.children, {"href": "https://www.google.com"})
        b = HTMLNode('h1', '1text', TestHTMLNode.children, {"href": "https://www.boot.dev"})
        self.assertNotEqual(a, b)

    def test_props_to_html(self):
        a = HTMLNode('h1', '1text', TestHTMLNode.children, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        result = a.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(result, expected)

    ### Leaf Node Tests ###

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me</a>')

    def test_leaf_to_html_no_tag_returns_raw(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

    def test_leaf_to_html_missing_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()