#!/usr/bin/env python3

from typing import List
from collections import defaultdict

import yaml
from tree_sitter import Parser, Language, Node

RE_LANGUAGE = Language("build/my-languages.so", "regex")

parser = Parser()
parser.set_language(RE_LANGUAGE)


def regexes(file: str = "regexes.yaml"):
    "iterate over all regexes in the ua-parser YAML file"
    ua = yaml.load(open(file, "r", encoding="utf8"), Loader=yaml.SafeLoader)
    for u in ua["user_agent_parsers"]:
        yield u["regex"]


def ngram(txt: str | bytes, size: int):
    "yield all ngrams"
    if len(txt) < size:
        yield txt
    else:
        for i in range(len(txt) - size + 1):
            yield txt[i : i + size]


def walk(node: Node, ngrams=None) -> set[str]:
    "Walk over regexp parsed file"
    if ngrams is None:
        ngrams = set()
    if node.type == "term":
        ok = True
        for n in node.children:
            ok = ok and n.type == "pattern_character"
        if ok and len(node.text) >= 3:
            nn = list(ngram(node.text.decode(), 3))
            ngrams.update(nn)
    for n in node.children:
        ngrams.union(walk(n, ngrams))
    return ngrams


def parse_ua(regex: str | bytes) -> List[str]:
    "Return ngrams from a regular expression"
    if isinstance(regex, str):
        regex = regex.encode("utf8")
    tree = parser.parse(regex)
    node = tree.root_node
    return walk(node)


def parse_all():
    idx = defaultdict(list)
    for i, r in enumerate(regexes()):
        ngrams = parse_ua(r)
        for n in ngrams:
            idx[n].append(i)
    return dict(idx)


if __name__ == "__main__":
    import json

    print(json.dumps(parse_all()))
