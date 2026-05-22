#!/usr/bin/env python3
import os

title_index = {}
wiki_dir = "/mnt/wiki_docs"

for filename in os.listdir(wiki_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(wiki_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            title_index[filename] = first_line

with open("titles.txt", 'w') as f:
    for fname, title in title_index.items():
        f.write(f"{fname}\t{title}\n")

print(f"Total títulos indexados: {len(title_index)}")
