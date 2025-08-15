from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:   # Skip non-text nodes
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter) # Split by delimiter
        if len(sections) % 2 == 0:  # Validate markdown syntax
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":   # Skip empty sections
                continue
            if i % 2 == 0:    # Even index = normal text
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:   # Odd index = formatted text
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)   # Merge results
    return new_nodes
