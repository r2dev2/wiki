import re
import sys

from bs4 import BeautifulSoup
from textblob import TextBlob


index = dict()
topics = set()
useless_chars = re.compile(r"[=|-|–|“|”|.| ]+")

def get_sentence_topics(sentence: str) -> set[str]:
    blob = TextBlob(sentence)
    return {*blob.noun_phrases.lemmatize()}

def get_topics(text: str) -> set[str]:
    topics = set()
    sentences = re.split(r"\n+", text)
    [*map(topics.update, map(get_sentence_topics, sentences))]
    return {*filter(bool, map(remove_useless_chars, topics))}

def remove_useless_chars(text: str) -> str:
    return re.sub(useless_chars, " ", text) \
        .strip() \
        .replace(" ’ ", "'")

def main():
    with open(sys.argv[1], "r") as fin:
        text = fin.read()

    combined_text = BeautifulSoup(text, "html.parser").text

    print(get_topics(combined_text))


if __name__ == "__main__":
    main()
