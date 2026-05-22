#!/usr/bin/env python3
import sys
import subprocess

def get_titles(bucket, prefix):
    titles = {}
    result = subprocess.run(
        ['aws', 's3', 'ls', f's3://{bucket}/{prefix}'],
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        filename = line.split()[-1]
        content = subprocess.run(
            ['aws', 's3', 'cp', f's3://{bucket}/{prefix}{filename}', '-'],
            capture_output=True, text=True
        )
        first_line = content.stdout.splitlines()[0].strip()
        titles[filename] = first_line
    return titles

def buscar(terminos, bucket, output_prefix, input_prefix):
    index = {}
    result = subprocess.run(
        ['aws', 's3', 'ls', f's3://{bucket}/{output_prefix}'],
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        fname = line.split()[-1]
        if not fname.startswith('part-'):
            continue
        part = subprocess.run(
            ['aws', 's3', 'cp', f's3://{bucket}/{output_prefix}{fname}', '-'],
            capture_output=True, text=True
        )
        for l in part.stdout.splitlines():
            parts = l.split('\t', 1)
            if len(parts) == 2:
                word, docs = parts
                index[word] = docs.split(', ')

    titles = get_titles(bucket, input_prefix)

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
            titulo = titles.get(doc, "Sin título")
            print(f'  {doc}  "{titulo}"  ({hits} término(s))')
    else:
        print("  Sin resultados.")

buscar(
    [t.lower() for t in sys.argv[1:]],
    bucket="lab03-indice-invertido",
    output_prefix="output2/",
    input_prefix="input2/"
)
