from enum import Enum


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