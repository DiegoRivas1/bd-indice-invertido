#!/usr/bin/env python3
import sys
import subprocess

def load_titles():
    titles = {}
    try:
        with open("titles.txt", 'r') as f:
            for line in f:
                parts = line.strip().split('\t', 1)
                if len(parts) == 2:
                    titles[parts[0]] = parts[1]
    except FileNotFoundError:
        pass
    return titles

def buscar(terminos):
    index = {}
    result = subprocess.run(
        ['aws', 's3', 'ls', 's3://lab03-indice-invertido/output_wiki_final/'],
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        fname = line.split()[-1]
        if not fname.startswith('part-'):
            continue
        part = subprocess.run(
            ['aws', 's3', 'cp', f's3://lab03-indice-invertido/output_wiki_final/{fname}', '-'],
            capture_output=True, text=True
        )
        for l in part.stdout.splitlines():
            parts = l.split('\t', 1)
            if len(parts) == 2:
                word, docs = parts
                index[word] = docs.split(', ')

    titles = load_titles()

    resultados = {}
    for termino in terminos:
        if termino in index:
            for doc in index[termino]:
                resultados[doc] = resultados.get(doc, 0) + 1

    ranking = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
    print(f"\nBúsqueda: {' '.join(terminos)}")
    print("-" * 50)
    if ranking:
        for doc, hits in ranking[:10]:
            titulo = titles.get(doc, doc.replace('_', ' ').replace('.txt', ''))
            print(f'  {doc}  "{titulo}"  ({hits} término(s))')
    else:
        print("  Sin resultados.")

buscar([t.lower() for t in sys.argv[1:]])
