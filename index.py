#!/usr/bin/env python3

from typing import List
from collections import defaultdict

import yaml
from tree_sitter import Parser, Language, Node

RE_LANGUAGE = Language("build/my-languages.so", "regex")

parser = Parser()
parser.set_language(RE_LANGUAGE)


class Regexes:
    def __init__(self, path: str = "regexes.yaml"):
        with open(path, "r", encoding="utf8") as f:
            self._data = yaml.load(f, Loader=yaml.SafeLoader)
        self._indexes = dict()

    def keys(self) -> list[str]:
        return self._data.keys()

    def index(self, key) -> dict[str, list[int]]:
        if key not in self._data:
            raise KeyError()
        if key not in self._indexes:
            idx = defaultdict(list)
            for i, r in enumerate(self._data[key]):
                ngrams = set()
                for t in extract_term(r['regex']):
                    if len(t) >= 3:
                        ngrams.update(ngram(t, 3))
                for n in ngrams:
                    idx[n].append(i)
            self._indexes[key] = dict(idx)
        return self._indexes[key]


def ngram(txt: str | bytes, size: int):
    "yield all ngrams"
    if len(txt) < size:
        yield txt
    else:
        for i in range(len(txt) - size + 1):
            yield txt[i : i + size]


def _walk(node: Node, terms=None) -> list[str]:
    "Walk over regexp parsed file"
    if terms is None:
        terms = list()
    if node.type == "term":
        ok = True
        for n in node.children:
            ok = ok and n.type == "pattern_character"
        if ok:
            terms.append(node.text.decode())
    for n in node.children:
        _walk(n, terms)  # terms is a pointer, not a value
    return terms


def extract_term(regex: str | bytes) -> List[str]:
    "Return terms from a regular expression"
    if isinstance(regex, str):
        regex = regex.encode("utf8")
    tree = parser.parse(regex)
    node = tree.root_node
    return _walk(node)


if __name__ == "__main__":
    import json
    import sys

    r = Regexes()
    for k in r.keys():
        p = r.index(k)
        print(k, file=sys.stderr)
        print("\t", len(r._data[k]), "regexes", file=sys.stderr)
        print("\t", len(p), "ngrams", file=sys.stderr)
        print(json.dumps(p))
