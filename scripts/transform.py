import sys

from markdown import markdown

def transform_markdown(md):
    return markdown(md, extensions=["extra"])

def transform_file(in_file, out_file):
    with open(in_file, "r") as fin:
        md = fin.read()

    with open(out_file, "w+") as fout:
        print(transform_markdown(md), file=fout)

def main():
    transform_file(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
