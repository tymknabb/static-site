
from inline_helpers import *
from block_helpers import *

def main():
    md = """
>Implying
>Further implying
>Literally projecting

Who are you quoting?
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    print(html)

main()