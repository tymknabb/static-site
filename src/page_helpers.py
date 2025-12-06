from os import listdir, mkdir, makedirs
from os.path import exists, join, isfile
from shutil import copy
from block_helpers import markdown_to_html_node


def copy_static_content(source, destination):
    if not exists(destination):
        mkdir(destination)

    for path in listdir(source):
        from_path = join(source, path)
        to_path = join(destination, path)
        print(f"Copying {from_path} to {to_path}...")
        if isfile(from_path):
            copy(from_path, to_path)
        else:
            copy_static_content(from_path, to_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            return title
    raise ValueError("Markdown contains no h1 heading.")

def generate_page(from_path, template_path, to_path):
    print(f"Generating page from {from_path} to {to_path} using {template_path}")
    with open(from_path) as s:
        markdown = s.read()
    with open(template_path) as t:
        index_html = t.read()

    title = extract_title(markdown)
    index_html = index_html.replace("{{ Title }}", title)

    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()
    index_html = index_html.replace("{{ Content }}", html_content)

    s.close()
    t.close()
    
    if not exists("./public"):
        makedirs("./public")
    with open(to_path, "a") as i:
        i.write(index_html + '\n')
