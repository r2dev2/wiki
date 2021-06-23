import sys
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


def main():
    transform_file(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
