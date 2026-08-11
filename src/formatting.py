from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            node_text = node.text
            split_text = node_text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("invalid markdown, formatted section not closed.")

            for i, item in enumerate(split_text):
                if not item:
                    continue
                if i % 2 == 0:
                    new_node_type = TextType.TEXT
                else:
                    new_node_type = text_type
                res_node = TextNode(item, new_node_type)
                new_nodes.append(res_node)

    return new_nodes
