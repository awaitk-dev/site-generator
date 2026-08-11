# print('hello world')
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from formatting import split_nodes_delimiter




def main():
    newNode = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(newNode)

    # node = TextNode("text `code block` word", TextType.TEXT)
    # node2 = TextNode("HTML", TextType.ITALIC)
    # new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
    # print(new_nodes)

main()