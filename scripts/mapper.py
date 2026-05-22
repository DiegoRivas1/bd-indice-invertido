#!/usr/bin/env python3
import sys
import os
import re

doc_id = os.environ.get("mapreduce_map_input_file", "unknown")
doc_name = os.path.basename(doc_id)

for line in sys.stdin:
    line = line.strip().lower()
    words = re.findall(r'[a-zA-Z]+', line)
    for word in words:
        if len(word) > 2:
            print(f"{word}\t{doc_name}")
