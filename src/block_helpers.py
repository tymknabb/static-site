from enum import Enum
from htmlnode import ParentNode
from textnode import TextType, TextNode
from inline_helpers import text_node_to_html_node, text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered_list"
    O_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    new_blocks = []
    raw_blocks = markdown.split("\n\n")
    for block in raw_blocks:
        if block == "":
            continue
        block = block.strip()
        new_blocks.append(block)
    
    return new_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ","### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.U_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.O_LIST

    return BlockType.PARAGRAPH

def collate_text(text):
    text_nodes = text_to_textnodes(text)
    sub_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        sub_nodes.append(html_node)

    return sub_nodes

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    block_lines = block.split("\n")
    html_nodes = []
    match block_type:
        case BlockType.PARAGRAPH:
            paragraph = " ".join(block_lines)
            children = collate_text(paragraph)
            return ParentNode("p", children)

        case BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            text = block[level + 1:]
            children = collate_text(text)
            return ParentNode(f"h{level}", children)

        case BlockType.CODE:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("Error: Invalid code block syntax.")
            text = block[4:-3]
            code_textnode = TextNode(text, TextType.TEXT)
            child_node = text_node_to_html_node(code_textnode)
            code = ParentNode("code", [child_node])
            return ParentNode("pre", [code])

        case BlockType.O_LIST:
            for item in block_lines:
                text = item[3:]
                children = collate_text(text)
                html_nodes.append(ParentNode("li", children))
            return ParentNode("ol", html_nodes)

        case BlockType.U_LIST:
            for item in block_lines:
                text = item[2:]
                children = collate_text(text)
                html_nodes.append(ParentNode("li", children))
            return ParentNode("ul", html_nodes)

        case BlockType.QUOTE:
            for line in block_lines:
                if not line.startswith(">"):
                    raise ValueError("Error: Invalid quote block.")
                html_nodes.append(line.lstrip(">").strip())
            text = " ".join(html_nodes)
            children = collate_text(text)
            return ParentNode("blockquote", children)

        case _:
            raise ValueError("Error: Must be a valid block type.")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children, None)
