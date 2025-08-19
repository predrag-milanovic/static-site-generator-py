def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")     # Split on double newlines
    filtered_blocks = []
    for block in blocks:
        if block == "":     # Skip empty blocks
            continue
        block = block.strip()   # Remove leading/trailing whitespace
        filtered_blocks.append(block)
    return filtered_blocks
