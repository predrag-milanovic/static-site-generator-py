import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"                 # Tests heading detection
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"            # Tests code block with triple backticks
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"     # Tests multi-line quote
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"           # Tests unordered list
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"         # Tests ordered list with sequential numbers
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"                 # Tests fallback to paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
