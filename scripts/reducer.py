#!/usr/bin/env python3
import sys

current_word = None
doc_set = set()

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split('\t', 1)
    if len(parts) != 2:
        continue
    word, doc = parts
    if word != current_word:
        if current_word:
            print(f"{current_word}\t{', '.join(sorted(doc_set))}")
        current_word = word
        doc_set = {doc}
    else:
        doc_set.add(doc)

if current_word:
    print(f"{current_word}\t{', '.join(sorted(doc_set))}")
