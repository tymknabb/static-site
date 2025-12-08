import re
from htmlnode import LeafNode
from textnode import TextType, TextNode


def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", " ", {"src": text_node.url, "alt": text_node.text})
		case _:
			raise Exception("Error: Must be a valid text type.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
		parts = []
		parts = node.text.split(delimiter)
		if len(parts) % 2 == 0:
			raise Exception("Invalid markdown syntax: missing closing delimiter.") 
		in_delimiter = False
		for part in parts:
			if in_delimiter:
				new_nodes.append(TextNode(part, text_type))
			elif part != "":
				new_nodes.append(TextNode(part, TextType.TEXT))
			in_delimiter = not in_delimiter
		
	return new_nodes

def extract_markdown(text, text_type):
	if text_type == TextType.IMAGE: 
		matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	elif text_type == TextType.LINK:
		matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def split_nodes(old_nodes, text_type):
	new_nodes = []
	excl = "!" if text_type == TextType.IMAGE else ""
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		node_text = old_node.text
		groups = extract_markdown(node_text, text_type)
		if groups == []:
			new_nodes.append(old_node)
			continue
		for group in groups:
			sections = node_text.split(f"{excl}[{group[0]}]({group[1]})", 1)
			if len(sections) != 2:
				raise ValueError(f"Invalid markdown, {text_type.value} not closed.")
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], TextType.TEXT))
			new_nodes.append(TextNode(group[0], text_type, group[1]))
			node_text = sections[1]
		if node_text != "":
			new_nodes.append(TextNode(node_text, TextType.TEXT))
	
	return new_nodes

def text_to_textnodes(text):
	old_nodes = [TextNode(text, TextType.TEXT)]
	nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes(nodes, TextType.IMAGE)
	nodes = split_nodes(nodes, TextType.LINK)

	return nodes