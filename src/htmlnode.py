class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        # Basic HTML node structure
        self.tag = tag            # HTML tag name (e.g., "p", "a")
        self.value = value        # Raw text content
        self.children = children  # List of child HTMLNodes
        self.props = props        # Dictionary of tag attributes

    def to_html(self):
        # Base method to be implemented by child classes
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        # Convert props dictionary to HTML attribute string
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        # Debug-friendly representation
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    # Leaf nodes cannot have children - forced to None
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        # Render leaf node as HTML string
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:    # Raw text case
            return self.value
        # Standard HTML tag with attributes
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"