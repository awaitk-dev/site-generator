

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        output = ""
        if not self.props:
            return output
        for key in self.props:
            output += f' {key}="{self.props[key]}"'
        return output

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        # All leaf nodes must have a value
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        # If there's no tag, return the raw text value
        if self.tag is None:
            return str(self.value)

        # Otherwise render an HTML tag with optional props
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        # ParentNode must have children (value is not used for ParentNode)
        if self.children is None:
            raise ValueError("ParentNode must have children")

        # If there's no tag, the spec requires raising a ValueError
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        # Render children recursively
        rendered_children = ""
        for child in self.children:
            # Expect each child to implement to_html()
            rendered_children += child.to_html()

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{rendered_children}</{self.tag}>"

