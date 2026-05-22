#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os
import re
import sys

output_dir = "/mnt/wiki_docs"
os.makedirs(output_dir, exist_ok=True)

namespace = "{http://www.mediawiki.org/xml/export-0.11/}"
count = 0
max_docs = 5000  # suficiente para el lab

context = ET.iterparse("/mnt/simplewiki-latest-pages-articles.xml", events=("end",))

for event, elem in context:
    if elem.tag == f"{namespace}page":
        title = elem.findtext(f"{namespace}title", "")
        text_elem = elem.find(f".//{namespace}text")
        text = text_elem.text if text_elem is not None and text_elem.text else ""

        # filtrar redirecciones
        if text.strip().lower().startswith("#redirect"):
            elem.clear()
            continue

        # limpiar markup wiki básico
        text = re.sub(r'\[\[([^\]|]*\|)?([^\]]*)\]\]', r'\2', text)
        text = re.sub(r'\{\{[^\}]*\}\}', '', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r"'{2,}", '', text)
        text = re.sub(r'==+([^=]+)==+', r'\1', text)
        text = re.sub(r'\s+', ' ', text).strip()

        if len(text) < 200:
            elem.clear()
            continue

        filename = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')[:60]
        filepath = os.path.join(output_dir, f"{filename}.txt")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(title + "\n")
            f.write(text[:5000])  # primeros 5000 chars por artículo

        count += 1
        if count % 500 == 0:
            print(f"Procesados: {count} artículos...")
            sys.stdout.flush()

        if count >= max_docs:
            break

        elem.clear()

print(f"Total: {count} artículos generados en {output_dir}")
