import json
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


def transform_markdown(md, article_title):
    article = center_images(markdown(md, extensions=["extra"]))
    return f"""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>{article_title} - ALSWiki</title>
        <link rel="stylesheet" href="../../index.css" />
        <script defer src="../../index.js"></script>
    </head>

    <body>
        <main class="md">
        <div class="article-search">
            <input type="text" placeholder="Search ALSWiki" />
        </div>
            {article}
        <main>
    </body>
</html>
    """


def transform_file(in_file, out_file):
    with open(in_file, "r") as fin:
        md = fin.read()

    article_title = filename_to_article_name(in_file)

    with open(out_file, "w+") as fout:
        print(transform_markdown(md, article_title), file=fout)


def is_markdown(fp):
    return fp[-3:] == ".md"


def filename_to_article_name(fname: str) -> str:
    return Path(fname).stem.replace("_", " ")


def main():
    if len(sys.argv) > 2:
        transform_file(sys.argv[1], sys.argv[2])
        return

    with suppress(FileExistsError):
        os.mkdir("__dist__")

    articles = []

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
            name = filename_to_article_name(filename)
            transform_file(Path(dirname) / filename, (root_dir / filename).with_suffix(".html"))
            articles.append(name)

    with open(Path("__dist__") / "articles.json", "w+") as fout:
        json.dump(articles, fout)


if __name__ == "__main__":
    main()
