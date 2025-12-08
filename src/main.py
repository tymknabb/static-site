from inline_helpers import *
from block_helpers import *
from page_helpers import *
from os.path import exists
from shutil import rmtree
from sys import argv

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_markdown = "./content"
template_file = "./template.html"

def main():
    basepath = "/"
    if len(argv) > 1:
        basepath = argv[1]

    if exists(dir_path_public):
        rmtree(dir_path_public) 

    copy_static_content(dir_path_static, dir_path_public)
    generate_pages_recursive(basepath, dir_path_markdown, template_file, dir_path_public)

main()