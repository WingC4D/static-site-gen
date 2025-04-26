from text_to_textnodes import BlockType, markdown_to_blocks, block_to_block_type, TextNode, TextType, re, text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node


        

def generate_page(from_path: str, template_path: str, dst_path: str) -> None:
    print(f'Generating page from {from_path} to {dst_path} using {template_path}')
    with open(from_path, 'r') as rf, open(template_path, 'r') as tmp_f, open(dst_path,'w') as wf:
        rf_contents = rf.read()
        tmp_contents = tmp_f.read()
        html_str = markdown_to_html_node(rf_contents).to_html()
        title = extract_title(rf_contents)
        tmp_contents = title.join(tmp_contents.split(r'{{ Title }}'))
        tmp_contents = html_str.join(tmp_contents.split(r'{{ Content }}'))
        wf.write(str(tmp_contents))

def extract_title(markdown: str) -> str:
    title_as_list = [' '.join(block.split()[1:])
                          for block in markdown_to_blocks(markdown)
                          if block_to_block_type(block) is BlockType.HEADING
                          if find_heading_num(block) == 'h1'
                          ]
    if not any(word for word in markdown.split() for word in '#'.split()):
        raise ValueError('The Block spliter Failed')
    return title_as_list[0]

def markdown_to_html_node(markdown: str) -> HTMLNode:
    children_nodes = [block_to_htmlnodes(block, block_to_block_type(block))
             for block in markdown_to_blocks(markdown)]
    return ParentNode('div', children_nodes)

def block_to_htmlnodes (block: str, block_type: BlockType) -> HTMLNode:
    children: list = [text_node_to_html_node(textnode) for textnode in text_to_textnodes(block) if textnode.text_type in TextType]
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode('p', children)
        case BlockType.CODE:
            return ParentNode('pre', [text_node_to_html_node(TextNode(''.join(block.strip('```')), TextType.CODE))])
        
        case BlockType.HEADING:              
            return ParentNode(find_heading_num(block),[text_node_to_html_node(node) for node in text_to_textnodes(' '.join(block.split()[1:]))])

        case BlockType.QUOTE: 
            return ParentNode('blockquote', quoteblock_to_htmlnodes(block))

        case BlockType.ORDERED_LIST:
            return ParentNode('ol',list_to_htmlnodes(block))

        case BlockType.UNORDERED_LIST:
            return ParentNode('ul', list_to_htmlnodes(block))

   
    return children

def quoteblock_to_htmlnodes(block: str) -> list[LeafNode]:
    children = [text_node_to_html_node(node)
                        for line in block.split('\n')
                        for node in text_to_textnodes(' '.join(line.split()[1:]))
                        if line.strip()] 
    return children

def list_to_htmlnodes(block: str) -> list[ParentNode]:
    li_nodes = [ParentNode('li',[text_node_to_html_node(node) 
                                 for node in text_to_textnodes(' '.join(line.split()[1:]))])
                for line in block.split('\n') 
                if line.strip() and (line.split()[0].endswith('.') 
                                     or line.split()[0] == '-')]
    return li_nodes

def find_heading_num(heading_block_text: str) -> str:
    
    '''
    This Function takes a Heading Block's text and returns a Tag correlating to which type of higharchical value the heading holds
    
    ### Args:
        heading_block_text:
            The Text it sounds like
    
    ### Returns:
        An HTML tag based on the inputed  Headings block text
    '''
    block_token_lst = heading_block_text.split()
    
    return f'h{len(block_token_lst[0])}'
