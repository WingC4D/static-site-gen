from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str| None, text_type: TextType) -> list[TextNode]:
    '''
    Splits text nodes based on a delimiter, creating new nodes with alternating text types.
    Args:
        old_nodes: A list of TextNode objects to process.
        delimiter: The string delimiter (e.g., "*", "`", "_") used for splitting.
                   This implementation assumes simple delimiters, not complex regex patterns
                   that might match parts of words unintentionally unless escaped properly
                   in the calling code (e.g., passing r'\*' instead of just '*').
                   The delimiter itself is consumed by the split.
        text_type: The TextType to apply to the text segments found *between* the delimiters.
    Returns:
        A new list of TextNode objects where text nodes have been split.
    Raises:
        ValueError: If an unmatched delimiter is found within a text node's content.
        ValueError: If the User input in the delimter Arg is not found in the TextType Enum
    '''
    if text_type not in TextType:
        raise ValueError(f'The "text_type" Argument MUST be a valid TextType!\nFor Refrence look at the TextType Class Docs.')
    
    new_nodes= []
    
    for node in old_nodes:  
        # Check if the node is a TextNode and skips it if its not a text node.
        if node.text_type is not TextType.Text:
            continue
        if delimiter is None or delimiter == '' or delimiter not in node.text:
            new_nodes.append(node)
        split_text = node.text.split(delimiter)
        for i, snippet in enumerate(split_text):
            if i % 2 == 0:
                print(snippet)