import re

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


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:     # Skip non-text nodes
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)     # Extract all images
        if len(images) == 0:        # No images? Keep original node
            new_nodes.append(old_node)
            continue
        for image in images:        # Split text around each image
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:  # Validate markdown syntax
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":   # Add text before image
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            # Add image node
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]     # Remaining text
        if original_text != "":     # Add trailing text
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: # Skip non-text nodes
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)   # Extract all links
        if len(links) == 0:     # No links? Keep original node
            new_nodes.append(old_node)
            continue
        for link in links:      # Split text around each link
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:      # Validate markdown syntax
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":       # Add text before link
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))     # Add link node
            original_text = sections[1]     # Remaining text
        if original_text != "":     # Add trailing text
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

# Added regex pattern to extract markdown images
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)     # Returns list of (alt, url) tuples
    return matches

# Added regex pattern to extract markdown links
def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)     # Returns list of (text, url) tuples
    return matches