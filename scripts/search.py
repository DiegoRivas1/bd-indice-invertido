#!/usr/bin/env python3
import sys
import subprocess

def buscar(terminos):
    index = {}
    for i in range(5):
        result = subprocess.run(
            ['aws', 's3', 'cp', f's3://lab03-indice-invertido/output/part-0000{i}', '-'],
            capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
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
    print("-" * 40)
    if ranking:
        for doc, hits in ranking:
            print(f"  {doc}  ({hits} término(s) coinciden)")
    else:
        print("  Sin resultados.")

buscar([t.lower() for t in sys.argv[1:]])
