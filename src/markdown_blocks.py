from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")     # Split on double newlines
    filtered_blocks = []
    for block in blocks:
        if block == "":     # Skip empty blocks
            continue
        block = block.strip()   # Remove leading/trailing whitespace
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")       # Split block into individual lines

    # Check for heading (1-6 # followed by space)
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # Check for code block (starts and ends with ```)
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    # Check for quote block (every line starts with >)
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):    # Any line without > fails quote
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    # Check for unordered list (every line starts with - )
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):   # Any line without - fails
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    # Check for ordered list (numbered 1., 2., 3., etc.)
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):   # Check sequential numbering
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    # Default to paragraph if no other type matches
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)       # Split into blocks
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)   # Convert each block to HTML
        children.append(html_node)
    return ParentNode("div", children, None)    # Wrap in div container


def block_to_html_node(block):
    block_type = block_to_block_type(block) # Determine block type
    # Route to appropriate converter based on block type
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)    # Convert to TextNodes
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)   # Convert to HTMLNodes
        children.append(html_node)
    return children

# Paragraph converter - handles inline markdown
def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)     # Join multiline paragraphs
    children = text_to_children(paragraph)  # Process inline markdown
    return ParentNode("p", children)

# Heading converter - extracts level and text
def heading_to_html_node(block):
    level = 0
    for char in block:      # Count # characters for heading level
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]       # Extract text after #
    children = text_to_children(text)   # Process inline markdown
    return ParentNode(f"h{level}", children)    # Create h1-h6 tag

# Code block converter - preserves raw content
def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]      # Remove triple backticks
    raw_text_node = TextNode(text, TextType.TEXT)   # Create raw text node
    child = text_node_to_html_node(raw_text_node)   # Convert to HTML (no inline processing)
    code = ParentNode("code", [child])  # Wrap in <code>
    return ParentNode("pre", [code])    # Wrap in <pre>

# Ordered list converter
def olist_to_html_node(block):
    items = block.split("\n")   # Split into list items
    html_items = []
    for item in items:
        text = item[3:] # Remove "X. " prefix
        children = text_to_children(text)   # Process inline markdown
        html_items.append(ParentNode("li", children))   # Create <li>
    return ParentNode("ol", html_items) # Wrap in <ol>

# Unordered list converter
def ulist_to_html_node(block):
    items = block.split("\n")   # Split into list items
    html_items = []
    for item in items:
        text = item[2:] # Remove "- " prefix
        children = text_to_children(text)   # Process inline markdown
        html_items.append(ParentNode("li", children))   # Create <li>
    return ParentNode("ul", html_items) # Wrap in <ul>

# Quote block converter
def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):    # Validate quote syntax
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())  # Remove > and trim
    content = " ".join(new_lines)   # Join quote lines
    children = text_to_children(content)    # Process inline markdown
    return ParentNode("blockquote", children)   # Wrap in <blockquote>