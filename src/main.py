from inline_helpers import *
from block_helpers import *
from page_helpers import *
from os.path import exists
from shutil import rmtree
from sys import argv

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_markdown = "./content"
template_file = "./template.html"
basepath = argv[1] or "/"

def main():
    if exists(dir_path_public):
        rmtree(dir_path_public)

    copy_static_content(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_markdown, template_file, dir_path_public)

main()