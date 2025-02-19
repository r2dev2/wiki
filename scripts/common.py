import os
from pathlib import Path

def visit_files_in_dir(root, dir_exclude=lambda dname: False, file_exclude=lambda fname: False):
    def visit(func):
        for dirname, _, filenames in os.walk(root):
            if dir_exclude(dirname):
                continue

            for filename in filenames:
                if file_exclude(filename):
                    continue
                func(dirname, filename)

    return visit

def filename_to_article_name(fname: str) -> str:
    return Path(fname).stem.replace("_", " ")
