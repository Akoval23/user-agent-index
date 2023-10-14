# User agent index

Starting from works from Google,
Browserscope provides a list of regular expressions to extract some meanings of user agents, one of the headers sent by HTTP clients.

The rules was wrote before the machine learning era, for each user agent lines, you have to iterate over hundreds of regexp, and stop with the first match.

It's cute, deterministic but inneficient.

Lets add some index, and shortcut the path before iterating like a boar.

## Test it

The code uses poetry for managing the few python libraries.

tree-sitter is a generic parser tool, using agnostic rules that you can compile for your target language. For python, the tool build a dynamic library, a .so file. `build-parser.py` compiles the regex grammar.

    make

There is some unit tests, useful as code example and for hunting regressions.

The official tests fixtures from main ua-parser project are used, too.

    make test
