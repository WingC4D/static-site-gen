from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag:str | None = None, value:str | None = None,
                 props:dict | None = None, children:list | None = None ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        if self.tag is None and self.value is None and self.props is None and self.children is None:
            return 'HTMLNode(empty)'
        result= ""
        if self.tag is not None:
            result += f'Tag: {self.tag}, '
        if self.value is not None:
            result += f'Value: {self.value}, '
        if self.props is not None:
            result += f'Attributes: {self.props_to_html()}, '
        if self.children is not None:
            result += f'Children: {str(self.children)}'
        return f'HTMLNode({result.rstrip(", ")})'

    def to_html(self) -> str:
        raise NotImplementedError("Override with a child class!")
    
    def props_to_html(self) -> str:
        if self.props == None:
            return  ""
        attributes = []
        for key, value in self.props.items():
            attributes.append(f'{key}="{value}"')
        return str(" " + " ".join(attributes))
        
class LeafNode(HTMLNode):
    def __init__(self, tag: str| None = None , value :str | int | float = "", props: dict | None = None) -> None:
        super().__init__(tag, props)
        
        self.props = props
        self.tag = tag
        
        if value == None:
            raise ValueError("All LeafNodes MUST have a value!")
        
        if not isinstance(value,(str, int, float)):
            raise TypeError('Value MUST be of a TextType Object! \n(Valid Types: String, Integer or Float)')
        
        
        self.value = str(value)
    
    def __repr__(self) -> str:
        represantation = f'LeafNode(Tag: {self.tag}, Value: {self.value}'
        
        if self.props:
            represantation += f',  Attributes: {self.props_to_html()}'
        
        return f'{represantation})'

    def to_html(self) -> str:
        if self.tag == 'img' and not self.value:
            return f'<{self.tag}{self.props_to_html()}>'
        elif self.tag != 'code':
            self.value = ' '.join(self.value.split('\n'))
        else:
            self.value = self.value.lstrip('\n')
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props:dict | None = None) -> None:
        
        super().__init__(tag, props, children)
        
        self.props = props
        
        if not tag or not isinstance(tag, str):
            raise ValueError('All Parent Nodes MUST have at least one tag in them!\nValid Types: String.')
        
        if not tag:
            raise ValueError('All Parent Nodes MUST have at least one (1) Tag')
        
        if not children or not isinstance(children, list):
            raise  ValueError('All Chilren Nodes MUST be of Object Type: list')
        
        if children == []:
            raise ValueError('All Children Nodes MUST have at least one (1) Child Node')
        
        self.tag = tag
        self.children = children

    def to_html(self) -> str:
        
        output = f'<{self.tag}{self.props_to_html()}>'
        
        for child in self.children:
            output += child.to_html()
        
        output += f'</{self.tag}>'
        
        return output
        
def text_node_to_html_node(text_node : TextNode, list: bool | None = None) -> LeafNode:
    """
    This function takes a Text Node and turns it into an HTML LeafNode.
    ### Args: 
        text_node: An object of type TextNode.
    ### Returns: 
        A LeafNode type object based on the input TextNode.
    ### Raises:
        A ValueError if the input Textnode's TextType is not found in the TextType Enum
    """
    if text_node.text_type not in TextType:
        raise ValueError('Text Type MUST be a valid HTML Format/Type!\nAvailable Text Types: TEXT,\nBOLD,\nITALIC,\nIMAGE,\nLINK,\nCODE')
        
    match (text_node.text_type):
        
        case (TextType.TEXT):
            return LeafNode(None , value = text_node.text)
        
        case(TextType.BOLD):
            return LeafNode('b', text_node.text)
        
        case(TextType.ITALIC):
            return LeafNode('i', text_node.text)
        
        case(TextType.CODE):
            return LeafNode('code', text_node.text)
        
        case(TextType.LINK):
            return LeafNode('a', text_node.text, {'href' : text_node.url} )
        
        case(TextType.IMAGE):
            return LeafNode('img', '', {'src' : text_node.url, 'alt' : text_node.text})    