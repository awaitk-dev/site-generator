import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
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

    def test_to_html_multiple_children(self):
        c1 = LeafNode("span", "one")
        c2 = LeafNode("i", "two")
        c3 = LeafNode(None, "three")
        parent = ParentNode("p", [c1, c2, c3])
        self.assertEqual(parent.to_html(), "<p><span>one</span><i>two</i>three</p>")

    def test_to_html_nested_parentnodes(self):
        inner = ParentNode("ul", [LeafNode("li", "item1"), LeafNode("li", "item2")])
        outer = ParentNode("div", [inner])
        self.assertEqual(outer.to_html(), "<div><ul><li>item1</li><li>item2</li></ul></div>")

    def test_to_html_with_props(self):
        child = LeafNode("a", "link", {"href": "https://example.com"})
        parent = ParentNode("div", [child], {"id": "main"})
        self.assertEqual(parent.to_html(), '<div id="main"><a href="https://example.com">link</a></div>')

    def test_to_html_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_to_html_missing_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "x")]).to_html()


if __name__ == "__main__":
    unittest.main()
