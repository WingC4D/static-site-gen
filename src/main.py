from os import path, listdir,mkdir
from shutil import copy, rmtree
from markdown_to_html_node import *


def main():
    dir_to_files('static', 'public')
    generate_page('content/index.md', 'template.html', 'public/index.html')
    dir_to_files('content', 'public')
    generate_pages_recursive('content', 'template.html', 'public')


def generate_pages_recursive(dir_path_content: str, template_plath: str, dest_dir_path: str) -> None:
    content_items_lst = listdir(dir_path_content)
    for item in content_items_lst:
        candidate_path = path.join(dir_path_content, item)
        dest_candidate_path = path.join(dest_dir_path, item)
        if path.isfile(candidate_path) and candidate_path.split('.')[1] == 'md':
            dest_candidate_path = path.join(dest_dir_path, f'{item.rstrip('md')}html')
            with open(candidate_path, 'r') as rf, open(template_plath, 'r') as tmp_f, open(dest_candidate_path, 'w') as wf:
                md = rf.read()
                html_str = markdown_to_html_node(md).to_html()

                title = extract_title(md)
                wf.write(tmp_f.read().replace(r'{{ Content }}', html_str).replace(r'{{ Title }}', title))
        elif path.isdir(candidate_path):
            generate_pages_recursive(candidate_path, template_plath, dest_candidate_path)
        continue
                
                                

def dir_to_files(dir_path: str, dst_path: str) -> list[str]:
    if not path.isfile(dst_path) and not path.isdir(dir_path):
        for i, dir in enumerate(dst_path.split('/')):
            if not path.isdir(dir) and i > len(dst_path.split('/')-1):
                print(path.isdir('/'.join(dst_path.split('/')[:i])))
            
    dir_items = listdir(dir_path)
    for item in dir_items:
        if path.isfile(path.join(dir_path, item)):
            copy(path.join(dir_path, item), dst_path)
        elif path.isdir(path.join(dir_path, item)):
            mkdir(path.join(dst_path, item))
            print(path.isdir(path.join(dst_path, item)))
            print(dir_to_files(path.join(dir_path, item), path.join(dst_path, item)))
    return listdir(dst_path)


if __name__ == "__main__":
    main()