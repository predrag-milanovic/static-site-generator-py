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
