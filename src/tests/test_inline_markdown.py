import unittest

from textnode import *
from htmlnode import *
from formatting import split_nodes_delimiter


class TestInlineMarkdown(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        result = split_nodes_delimiter([node, node2], "*", TextType.BOLD)
        self.assertIsNotNone(len(result) == 2)

    def test_base(self):
        node = TextNode("text `code block` word", TextType.TEXT)
        node2 = TextNode("HTML", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertTrue(len(new_nodes) == 4)

    def test_splits_text_on_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_leaves_non_text_nodes_unchanged(self):
        node = TextNode("plain", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)

        self.assertEqual(new_nodes, [node])

    def test_returns_original_node_when_delimiter_not_found(self):
        node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)

        self.assertEqual(new_nodes, [TextNode("plain text", TextType.TEXT)])

    def test_raises_for_unclosed_delimiter(self):
        node = TextNode("text with `unclosed", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_can_be_called_multiple_times_for_different_delimiters(self):
        node = TextNode("A *bold* and _italic_ example", TextType.TEXT)
        after_bold = split_nodes_delimiter([node], "*", TextType.BOLD)
        after_italic = split_nodes_delimiter(after_bold, "_", TextType.ITALIC)

        self.assertEqual(after_italic[0], TextNode("A ", TextType.TEXT))
        self.assertEqual(after_italic[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(after_italic[2], TextNode(" and ", TextType.TEXT))
        self.assertEqual(after_italic[3], TextNode("italic", TextType.ITALIC))
        self.assertEqual(after_italic[4], TextNode(" example", TextType.TEXT))


if __name__ == "__main__":
    unittest.main()