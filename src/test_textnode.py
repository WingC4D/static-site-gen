import unittest
from markdown_to_html_node import *
from text_to_textnodes import split_nodes_delimiter, split_nodes_link, split_nodes_image

class TestTextNode(unittest.TestCase):
    def test_eq_text(self):
        node = TextNode("the toyota corola is a lovely family automobile used all over the world", TextType.BOLD)
        node2 = TextNode("the toyota corola is a lovely family automobile used all over the world", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_text_type(self):
        node = TextNode("hello world!", TextType.TEXT)
        node2 = TextNode("hello world!", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("The Best Code Learning Platform", TextType.LINK, "https://boot.dev")
        node2 = TextNode("The Best Code Learning Platform", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)
    
    def test_eq_empty_url(self):
        node = TextNode("Yo mama is a world champ in DEEZ seeking", TextType.BOLD)
        node2 = TextNode("Yo mama is a world champ in DEEZ seeking", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_text(self):
        node = TextNode("Yo mama is a world champ in DEEZ seeking", TextType.BOLD)
        node2 = TextNode("the toyota corola is a lovely family automobile used all over the world", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("hello world!", TextType.TEXT)
        node2 = TextNode("hello world!", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("The Best Code Learning Platform", TextType.LINK, "https://boot.dev")
        node2 = TextNode("The Best Code Learning Platform", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_text_breakdown_bold(self):
        old_nodes = [TextNode("This is text with a **bold** word", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, '**', TextType.BOLD), [TextNode("This is text with a ", TextType.TEXT),
                                                                                 TextNode("bold", TextType.BOLD),
                                                                                 TextNode(" word", TextType.TEXT)])
    
    def test_text_breakdown_italic(self):
        old_nodes = [TextNode("This is text with an _italic_ word", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter(old_nodes,'_', TextType.ITALIC), [TextNode("This is text with an ", TextType.TEXT),
                                                                                 TextNode("italic", TextType.ITALIC),
                                                                                 TextNode(" word", TextType.TEXT)])
    
    def test_text_breakdown_code(self):
        old_nodes = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, '`', TextType.CODE), [TextNode("This is text with a ", TextType.TEXT),
                                                                                TextNode("code block", TextType.CODE),  
                                                                                TextNode(" word", TextType.TEXT)])
   
    def test_text_breakdown_regular_text(self):
        old_nodes = [TextNode("This is plain text",  TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, None, TextType.TEXT), [TextNode("This is plain text", TextType.TEXT)])
    
    def test_text_breakdown_multipule_bold(self):
        old_nodes = [TextNode("This **bold1** and **bold2** ,here",  TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, '**', TextType.BOLD),[TextNode("This ", TextType.TEXT),
                                                                                TextNode("bold1", TextType.BOLD),
                                                                                TextNode(" and ", TextType.TEXT),
                                                                                TextNode("bold2", TextType.BOLD),
                                                                                TextNode(" ,here", TextType.TEXT)])
    
    def test_split_images_single_image(self):
        node = TextNode(
            "Text with one ![image](https://i.imgur.com/test.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text with one ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/test.png"),
            ]
        )

    def test_split_images_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ]
        )

    def test_split_images_no_images(self):
        node = TextNode("This is plain text without images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_split_images_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/start.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/start.png"),
                TextNode(" followed by text", TextType.TEXT),
            ]
        )

    def test_split_images_image_at_end(self):
        node = TextNode(
            "Text before ![image](https://i.imgur.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/end.png"),
            ]
        )

    def test_split_images_empty_alt_text(self):
        node = TextNode(
            "Text with ![](https://i.imgur.com/empty.png) image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/empty.png"),
                TextNode(" image", TextType.TEXT),
            ]
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("First node with ![image](https://i.imgur.com/first.png)", TextType.TEXT),
            TextNode("Second node without images", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("First node with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/first.png"),
                TextNode("Second node without images", TextType.TEXT),
            ]
        )

    def test_split_images_no_text_between_images(self):
        node = TextNode(
            "![first](https://i.imgur.com/1.png)![second](https://i.imgur.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("first", TextType.IMAGE, "https://i.imgur.com/1.png"),
                TextNode("second", TextType.IMAGE, "https://i.imgur.com/2.png"),
            ]
        )

    # Tests for split_nodes_link
    def test_split_links_single_link(self):
        node = TextNode(
            "Text with one [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text with one ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ]
        )

    def test_split_links_multiple_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and [another](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.LINK, "https://www.youtube.com"),
            ]
        )

    def test_split_links_no_links(self):
        node = TextNode("This is plain text without links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_links_link_at_start(self):
        node = TextNode(
            "[link](https://www.boot.dev) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" followed by text", TextType.TEXT),
            ]
        )

    def test_split_links_link_at_end(self):
        node = TextNode(
            "Text before [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ]
        )

    def test_split_links_empty_link_text(self):
        node = TextNode(
            "Text with [](https://www.boot.dev) link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://www.boot.dev"),
                TextNode(" link", TextType.TEXT),
            ]
        )

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("First node with [link](https://www.boot.dev)", TextType.TEXT),
            TextNode("Second node without links", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("First node with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode("Second node without links", TextType.TEXT),
            ]
        )

    def test_split_links_no_text_between_links(self):
        node = TextNode(
            "[first](https://www.boot.dev)[second](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("first", TextType.LINK, "https://www.boot.dev"),
                TextNode("second", TextType.LINK, "https://www.youtube.com"),
            ]
        )

    def test_split_links_mixed_with_images(self):
        node = TextNode(
            "Text with [link](https://www.boot.dev) and ![image](https://i.imgur.com/test.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ![image](https://i.imgur.com/test.png)", TextType.TEXT),
            ]
        )

    def test_mixed_markdown(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_plain_text(self):
        text = "This is plain text with no markdown"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [TextNode("This is plain text with no markdown", TextType.TEXT)]
        )

    def test_only_bold(self):
        text = "**bold text**"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [TextNode("bold text", TextType.BOLD)]
        )

    def test_only_italic(self):
        text = "_italic text_"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [TextNode("italic text", TextType.ITALIC)]
        )

    def test_only_code(self):
        text = "`code block`"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [TextNode("code block", TextType.CODE)]
        )

    def test_only_image(self):
        text = "![alt text](https://i.imgur.com/test.png)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [TextNode("alt text", TextType.IMAGE, "https://i.imgur.com/test.png")]
        )

    def test_only_link(self):
        text = "[link text](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [TextNode("link text", TextType.LINK, "https://boot.dev")]
        )

    def test_multiple_bold_and_italic(self):
        text = "This is **bold** and **another bold** with _italic_ text"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another bold", TextType.BOLD),
                TextNode(" with ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]
        )


    def test_images_and_links(self):
        text = "An ![image](https://i.imgur.com/test.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("An ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/test.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_empty_text(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode('', TextType.TEXT)])

    def test_mixed_delimiters_with_images(self):
        text = "Text with **bold** and ![image](https://i.imgur.com/test.png) and `code`"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/test.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ]
        )

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        print(blocks)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )
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

    def test_single_block(self):
        md = "# This is a heading"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["# This is a heading"]
        )

    def test_multiple_blocks_with_varied_types(self):
        md = """
# Heading 1

This is a **paragraph** with _formatting_.

- List item 1
- List item 2

> This is a blockquote
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "This is a **paragraph** with _formatting_.",
                "- List item 1\n- List item 2",
                "> This is a blockquote",
            ]
        )

    def test_excessive_newlines(self):
        md = """


This is a paragraph



Another paragraph with **bold**

- List item


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "Another paragraph with **bold**",
                "- List item",
            ]
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_only_whitespace(self):
        md = "\n\n  \n\n\t\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_line_blocks(self):
        md = "Line 1\n\nLine 2\n\nLine 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Line 1", "Line 2", "Line 3"]
        )

    def test_blocks_with_trailing_and_leading_whitespace(self):
        md = """
   # Heading with spaces   

  This is a paragraph  
  with multiple lines  

- List item 1  
- List item 2  

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with spaces",
                "This is a paragraph\nwith multiple lines",
                "- List item 1\n- List item 2",
            ]
        )

    def test_paragraph_with_internal_newlines(self):
        md = """
This is a paragraph
with internal newlines
and **formatting**

Another paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph\nwith internal newlines\nand **formatting**",
                "Another paragraph",
            ]
        )

    def test_mixed_empty_and_non_empty_blocks(self):
        md = """
First block

  

Second block

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["First block", "Second block"]
        )

    def test_heading_single_hash(self):
        # Tests a heading with one '#' followed by text
        block = "# Heading text"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_six_hashes(self):
        # Tests a heading with six '#' followed by text
        block = "###### Heading text"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_no_space(self):
        # Tests a block starting with '#' but no space (should be paragraph)
        block = "#No space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_basic(self):
        # Tests a basic code block with triple backticks
        block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_with_language(self):
        # Tests a code block with a language identifier
        block = "```python\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_empty(self):
        # Tests an empty code block
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_missing_end(self):
        # Tests a block starting with ``` but not ending with ``` (should be paragraph)
        block = "```\ncode\nnot_backticks"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_single_line(self):
        # Tests a single-line quote block
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multi_line(self):
        # Tests a multi-line quote block
        block = "> Quote line 1\n> Quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_not_starting_with_quote(self):
        # Tests a block with '>' in the middle (should be paragraph)
        block = "text > not a quote\n> quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_basic(self):
        # Tests a basic unordered list
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_single_item(self):
        # Tests an unordered list with one item
        block = "- Single item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space(self):
        # Tests a block with '-' but no space (should be paragraph)
        block = "-Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_basic(self):
        # Tests a basic ordered list starting with 1.
        block = "1. First item\n2. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        # Tests an ordered list with one item
        block = "1. Single item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_non_sequential(self):
        # Tests a list with numbers but not sequential (should be paragraph)
        block = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_space(self):
        # Tests a block with '1.' but no space (should be paragraph)
        block = "1.First\n2.Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_basic(self):
        # Tests a basic paragraph
        block = "This is a paragraph with **bold** text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_with_backticks(self):
        # Tests a paragraph containing ``` but not as a code block
        block = "Text with backticks```inside"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        # Tests an empty block (should be paragraph)
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_single_line_with_special_chars(self):
        # Tests a paragraph with special characters that might mimic other types
        block = "Not a list - or > quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2 with **bold**

### Heading 3

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b></h2><h3>Heading 3</h3><h6>Heading 6</h6></div>"
        )

    def test_quote(self):
        md = """
> This is a **quote** with _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>quote</b> with <i>italic</i> text</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- Item 1 with **bold**
- Item 2 with _italic_
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1 with <b>bold</b></li><li>Item 2 with <i>italic</i></li><li>Item 3</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. First item with `code`
2. Second item
3. Third item with **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item with <code>code</code></li><li>Second item</li><li>Third item with <b>bold</b></li></ol></div>"
        )

    def test_mixed_blocks(self):
        md = """
# Main Heading

This is a paragraph with **bold** text.

> A quote with _italic_ text

- List item 1
- List item 2 with `code`

```
Code block
with newlines
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Heading</h1><p>This is a paragraph with <b>bold</b> text.</p><blockquote>A quote with <i>italic</i> text</blockquote><ul><li>List item 1</li><li>List item 2 with <code>code</code></li></ul><pre><code>Code block\nwith newlines\n</code></pre></div>"
        )
    
    def test_single_block(self):
        md = "This is a **single** paragraph"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a <b>single</b> paragraph</p></div>")

    def test_inline_images_and_links(self):
        md = """
This is a paragraph with [a link](http://example.com) and ![an image](image.jpg)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with <a href="http://example.com">a link</a> and <img src="image.jpg" alt="an image"></p></div>'
        )

    def test_excessive_headings(self):
        md = "####### Too Many Hashes"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>####### Too Many Hashes</p></div>")


if __name__ == "__main__":
    unittest.main()