# print('hello world')
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode




def main():
    newNode = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    print(newNode)

main()