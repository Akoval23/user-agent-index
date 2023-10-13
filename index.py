#!/usr/bin/env python3

from typing import List
from collections import defaultdict
import re
import io

import yaml
from tree_sitter import Parser, Language, Node

RE_LANGUAGE = Language("build/my-languages.so", "regex")

parser = Parser()
parser.set_language(RE_LANGUAGE)


NGRAM_SIZE = 4


class Index:
    def __init__(self, regexes) -> None:
        self.regexes = regexes
        idx = defaultdict(list)
        for i, r in enumerate(regexes):
            ngrams = set()
            for t in extract_term(r["regex"]):
                if len(t) >= NGRAM_SIZE:
                    ngrams.update(ngram(t, NGRAM_SIZE))
            for n in ngrams:
                idx[n].append(i)
        self.ngrams = dict(idx)

    def _ngram_idx(self, key: str) -> list[int]:
        "all sorted regex ids indexed throught ngrams"
        regexes = set()
        for n in set(ngram(key, NGRAM_SIZE)):
            if n not in self.ngrams:
                continue
            regexes.update(self.ngrams[n])
        l = list(regexes)
        l.sort()
        return l

    def search(self, key: str):
        for i in self._ngram_idx(key):
            if "_re" not in self.regexes[i]:
                self.regexes[i]["_re"] = re.compile(self.regexes[i]["regex"])
            match = self.regexes[i]["_re"].search(key)
            if match is not None:
                if "family_replacement" not in self.regexes[i]:
                    return match.group(1)
                else:
                    txt = self.regexes[i]["family_replacement"]
                    if len(match.groups()) > 1:
                        txt = txt.replace("$1", match.group(1))
                    return txt
        return None


def regexes(path: str = "regexes.yaml"):
    indexes = dict()
    with open(path, "r", encoding="utf8") as f:
        for k, v in yaml.load(f, Loader=yaml.SafeLoader).items():
            indexes[k] = Index(v)
    return indexes


def ngram(txt: str | bytes, size: int):
    "yield all ngrams"
    if len(txt) < size:
        yield txt
    else:
        for i in range(len(txt) - size + 1):
            yield txt[i : i + size]


def _walk(node: Node, terms: set[str]) -> set[str]:
    "Walk over regexp parsed file"
    if node.type == "term":
        term = io.BytesIO()
        for n in node.children:
            if n.type == "pattern_character":
                term.write(n.text)
            else:
                if term.tell() > 0:
                    term.seek(0)
                    terms.add(term.read().decode())
                    term = io.BytesIO()
        if term.tell() > 0:
            term.seek(0)
            terms.add(term.read().decode())
    for n in node.children:
        _walk(n, terms)  # terms is a pointer, not a value
    return terms


def extract_term(regex: str | bytes) -> set[str]:
    "Return terms from a regular expression"
    if isinstance(regex, str):
        regex = regex.encode("utf8")
    tree = parser.parse(regex)
    node = tree.root_node
    # print(node.sexp())
    return _walk(node, set())


if __name__ == "__main__":
    import json
    import sys

    r = regexes("./vendor/uap-core/regexes.yaml")
    for k, idx in r.items():
        print(k, file=sys.stderr)
        print("\t", len(idx.regexes), "regexes", file=sys.stderr)
        print("\t", len(idx.ngrams), "ngrams", file=sys.stderr)
        print(json.dumps(idx.ngrams))
