import unittest
from htmlnode import *

class TestHTMLNodes(unittest.TestCase):
    def test_node_repr(self):
        node = HTMLNode("a", "hi", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(repr(node), 'HTMLNode(Tag: a, Value: hi, Attributes:  href="https://www.google.com" target="_blank")')

    def test_node_props_to_html(self):
        node = HTMLNode("a", "hi", {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_node_tag(self):
        node = HTMLNode('p', 'Cause it be all the way... and yo mama is gay...', {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(node.tag, "p")

    def test_node_value(self):
        node = HTMLNode('b', 'ICH MAG BIER, B E R, MOMA SAGT BITTE SAUF WINGER')
        self.assertEqual(node.value, 'ICH MAG BIER, B E R, MOMA SAGT BITTE SAUF WINGER')

    def test_node_children(self):
        node = HTMLNode('p', 'Cause it be all the way... and yo mama is gay...', {"href": "https://www.google.com","target": "_blank"}, [HTMLNode(tag ='b')])
        self.assertEqual(repr(node), 'HTMLNode(Tag: p, Value: Cause it be all the way... and yo mama is gay..., Attributes:  href="https://www.google.com" target="_blank", Children: [HTMLNode(Tag: b)])')

    def test_leaf_to_html_p(self):
        node = LeafNode(tag = 'p', value = 'Hello, world!')
        self.assertEqual(node.to_html(),'<p>Hello, world!</p>')
    
    def test_leaf_to_html_No_Value(self):
        node = LeafNode('b',)
        try:
            node.to_html()
        except:                             
            print('The Value data member is required in a LeafNode:')
            Exception(ValueError('The Value data member is required in a LeafNode!'))    
    
    def test_leaf_to_html_b(self):
        node = LeafNode('b', 'Yo mama Gay!')
        self.assertEqual(node.to_html(), '<b>Yo mama Gay!</b>')

    def test_leaf_to_html_with_attributes(self):
        node = LeafNode('a', 2345235, {'href': 'https://www.GoonersNation.com'})
        self.assertEqual(node.to_html(), '<a href="https://www.GoonersNation.com">2345235</a>')
    
    def test_leaf_to_html_h1_and_attributes(self):
        node = LeafNode("h1", 'You Are A Dirty Rat and I Can Prove It Mathematically', props = {'href': 'https://www.GoonersNation.com'},)
        self.assertEqual('<h1 href="https://www.GoonersNation.com">You Are A Dirty Rat and I Can Prove It Mathematically</h1>', node.to_html())

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",)

    def test_to_html_crazy_time(self):
        child_node = LeafNode("b", "grandchild")
        child_node2 = LeafNode("span", "friesch bam maken ales rechts")
        child_node3 =  LeafNode('b', 'Bam Bam get ya')
        parent_node = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), '<div><b>grandchild</b><span>friesch bam maken ales rechts</span><b>Bam Bam get ya</b></div>')

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_convert_text(self):
        text_node = TextNode("Just some plain text", TextType.TEXT)
        expected_leaf_node = LeafNode(tag=None, value="Just some plain text")
        actual_leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(actual_leaf_node.tag, expected_leaf_node.tag)
        self.assertEqual(actual_leaf_node.value, expected_leaf_node.value)
        self.assertEqual(actual_leaf_node.props, expected_leaf_node.props)
        self.assertEqual(actual_leaf_node.to_html(), "Just some plain text")

    def test_convert_bold(self):
        text_node = TextNode("Bold statement", TextType.BOLD)
        expected_leaf_node = LeafNode(tag="b", value="Bold statement")
        actual_leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(actual_leaf_node.tag, expected_leaf_node.tag)
        self.assertEqual(actual_leaf_node.value, expected_leaf_node.value)
        self.assertEqual(actual_leaf_node.props, expected_leaf_node.props)
        self.assertEqual(actual_leaf_node.to_html(), "<b>Bold statement</b>")

    def test_convert_italic(self):
        text_node = TextNode("Emphasized text", TextType.ITALIC)
        expected_leaf_node = LeafNode(tag="i", value="Emphasized text")
        actual_leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(actual_leaf_node.tag, expected_leaf_node.tag)
        self.assertEqual(actual_leaf_node.value, expected_leaf_node.value)
        self.assertEqual(actual_leaf_node.props, expected_leaf_node.props)
        self.assertEqual(actual_leaf_node.to_html(), "<i>Emphasized text</i>")

    def test_convert_code(self):
        text_node = TextNode("code_snippet = True", TextType.CODE)
        expected_leaf_node = LeafNode(tag="code", value="code_snippet = True")
        actual_leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(actual_leaf_node.tag, expected_leaf_node.tag)
        self.assertEqual(actual_leaf_node.value, expected_leaf_node.value)
        self.assertEqual(actual_leaf_node.props, expected_leaf_node.props)
        self.assertEqual(actual_leaf_node.to_html(), "<code>code_snippet = True</code>")

    def test_convert_link(self):
        text_node = TextNode("Visit Boot.dev", TextType.LINK, "https://boot.dev")
        expected_leaf_node = LeafNode(tag="a", value="Visit Boot.dev", props={"href": "https://boot.dev"})
        actual_leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(actual_leaf_node.tag, expected_leaf_node.tag)
        self.assertEqual(actual_leaf_node.value, expected_leaf_node.value)
        self.assertEqual(actual_leaf_node.props, expected_leaf_node.props)
        self.assertEqual(actual_leaf_node.to_html(), '<a href="https://boot.dev">Visit Boot.dev</a>')

    def test_convert_image(self):
        text_node = TextNode("A cool image", TextType.IMAGE, "/images/cool.png")
        expected_leaf_node = LeafNode(tag = "img", value = "", props = {"src": "/images/cool.png", "alt": "A cool image"})
        actual_leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(actual_leaf_node.tag, expected_leaf_node.tag)
        self.assertEqual(actual_leaf_node.value, expected_leaf_node.value)
        self.assertEqual(actual_leaf_node.props, expected_leaf_node.props)
        self.assertEqual(actual_leaf_node.to_html(), '<img src="/images/cool.png" alt="A cool image">')
