#!/usr/bin/env python3
import sys
import subprocess

TITULOS = {
    "doc1.txt": "Pride and Prejudice - Jane Austen",
    "doc2.txt": "Alice in Wonderland - Lewis Carroll",
    "doc3.txt": "The Adventures of Sherlock Holmes - Arthur Conan Doyle"
}

def buscar(terminos):
    index = {}
    for i in range(5):
        part = subprocess.run(
            ['aws', 's3', 'cp', f's3://lab03-indice-invertido/output/part-0000{i}', '-'],
            capture_output=True, text=True
        )
        for line in part.stdout.splitlines():
            parts = line.split('\t', 1)
            if len(parts) == 2:
                word, docs = parts
                index[word] = docs.split(', ')

    resultados = {}
    for termino in terminos:
        if termino in index:
            for doc in index[termino]:
                resultados[doc] = resultados.get(doc, 0) + 1

    ranking = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
    print(f"\nBúsqueda: {' '.join(terminos)}")
    print("-" * 50)
    if ranking:
        for doc, hits in ranking:
            titulo = TITULOS.get(doc, doc)
            print(f'  {doc}  "{titulo}"  ({hits} término(s))')
    else:
        print("  Sin resultados.")

buscar([t.lower() for t in sys.argv[1:]])
