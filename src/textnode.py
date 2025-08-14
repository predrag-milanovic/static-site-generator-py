from htmlnode import LeafNode
from enum import Enum


class TextType(Enum):
    # Enum defining all supported text types for conversion
    TEXT = "text"       # Plain text (no tag)
    BOLD = "bold"       # <b> tag
    ITALIC = "italic"   # <i> tag
    CODE = "code"       # <code> tag
    LINK = "link"       # <a> tag with href
    IMAGE = "image"     # <img> tag with src/alt


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    # Core logic
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)   # Raw text node
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)    # Bold text
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)    # Italic text
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text) # Code block
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})   # Hyperlink
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})   # Image
    raise ValueError(f"invalid text type: {text_node.text_type}")   # Validation
