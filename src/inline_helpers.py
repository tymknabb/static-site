import re
from textnode import TextType, TextNode
from htmlnode import LeafNode

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
			return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
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

def extract_markdown_images(text):
	matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def extract_markdown_links(text):
	matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def split_nodes_image(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
		node_text = node.text
		images = extract_markdown_images(node_text)
		if images == []:
			new_nodes.append(node)
			continue
		for image in images:
			sections = node_text.split(f"![{image[0]}]({image[1]})", 1)
			if len(sections) != 2:
				raise Exception("Invalid markdown, image not closed.")
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], TextType.TEXT))
			new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
			node_text = sections[1]
		if node_text != "":
			new_nodes.append(TextNode(node_text, TextType.TEXT))
	
	return new_nodes

def split_nodes_link(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
		node_text = node.text
		links = extract_markdown_links(node_text)
		if links == []:
			new_nodes.append(node)
			continue
		for link in links:
			sections = node_text.split(f"[{link[0]}]({link[1]})", 1)
			if len(sections) != 2:
				raise Exception("Invalid markdown, link not closed.")
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], TextType.TEXT))
			new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
			node_text = sections[1]
		if node_text != "":
			new_nodes.append(TextNode(node_text, TextType.TEXT))
	
	return new_nodes

def text_to_textnodes(text):
	old_nodes = [TextNode(text, TextType.TEXT)]
	nodes_bold_processed 	= split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
	nodes_italic_processed 	= split_nodes_delimiter(nodes_bold_processed, "_", TextType.ITALIC)
	nodes_code_processed 	= split_nodes_delimiter(nodes_italic_processed, "`", TextType.CODE)
	nodes_images_processed 	= split_nodes_image(nodes_code_processed)
	nodes_links_processed 	= split_nodes_link(nodes_images_processed)

	return nodes_links_processed