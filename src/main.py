from inline_helpers import *
from block_helpers import *
from page_helpers import *
from os.path import exists
from shutil import rmtree

dir_path_static = "./static"
dir_path_public = "./public"
markdown_path = "./content/index.md"
template_path = "./template.html"

def main():
    if exists(dir_path_public):
        rmtree(dir_path_public)

    copy_static_content(dir_path_static, dir_path_public)
    generate_page(markdown_path, template_path, f"{dir_path_public}/index.html")

main()