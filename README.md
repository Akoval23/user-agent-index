# User agent index

Starting from works from Google,
Browserscope provides a list of regular expressions to extract some meanings of user agents, one of the headers sent by HTTP clients.

The rules was wrote before the machine learning era, for each user agent lines, you have to iterate over hundreds of regexp, and stop with the first match.

It's cute, deterministic but inneficient.
