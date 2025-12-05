from os import listdir, mkdir
from os.path import exists, join, isfile
from shutil import copy, rmtree

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
    pass