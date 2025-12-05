from inline_helpers import *
from block_helpers import *
from page_helpers import *

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    if exists(dir_path_public):
        rmtree(dir_path_public)
    copy_static_content(dir_path_static, dir_path_public)

main()