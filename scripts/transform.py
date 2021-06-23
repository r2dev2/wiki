import os
import shutil
import sys
from contextlib import suppress
from pathlib import Path
from operator import attrgetter

from bs4 import BeautifulSoup
from markdown import markdown


def center_images(html: str):
    soup = BeautifulSoup(html, "html.parser")
    for p in map(attrgetter("parent"), soup.select("p > img")):
        p["align"] = "center"
    return str(soup)


def transform_markdown(md):
    article = center_images(markdown(md, extensions=["extra"]))
    return f"""
<html>
    <head>
        <title>Sample page</title>
        <link rel="stylesheet" href="./index.css" />
    </head>

    <body>
        <main>
            {article}
        <main>
    </body>
</html>
    """


def transform_file(in_file, out_file):
    with open(in_file, "r") as fin:
        md = fin.read()

    with open(out_file, "w+") as fout:
        print(transform_markdown(md), file=fout)


def is_markdown(fp):
    return fp[-3:] == ".md"


def main():
    if len(sys.argv) > 2:
        transform_file(sys.argv[1], sys.argv[2])
        return

    with suppress(FileExistsError):
        os.mkdir("__dist__")
    shutil.copy("index.css", Path("__dist__") / "index.css")

    for dirname, _, filenames in os.walk("."):
        if dirname[:3] == "./." or dirname[:10] == "./__dist__":
            continue

        files = [*filter(is_markdown, filenames)]
        if not files:
            continue

        root_dir = Path("__dist__") / dirname

        with suppress(FileExistsError):
            os.mkdir(root_dir)

        for filename in files:
            transform_file(Path(dirname) / filename, (root_dir / filename).with_suffix(".html"))


if __name__ == "__main__":
    main()
