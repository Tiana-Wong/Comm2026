#!/usr/bin/env python3
"""Compute word counts for each abstract in the dataset.

Reads: /workspaces/Comm2026/demo/lab1/input/AI_mental_health.csv
Writes: /workspaces/Comm2026/demo/lab1/output/AI_mental_health_with_wordcount.csv

Usage: python3 word_count.py
"""
import csv
import os
import re
from pathlib import Path


BASE = Path(__file__).resolve().parent
INPUT = BASE / "input" / "AI_mental_health.csv"
OUTPUT_DIR = BASE / "output"
OUTPUT = OUTPUT_DIR / "AI_mental_health_with_wordcount.csv"


def count_words(text: str) -> int:
    if not text:
        return 0
    # Count word-like tokens (letters, numbers, underscores)
    return len(re.findall(r"\b\w+\b", text))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not INPUT.exists():
        print(f"Input file not found: {INPUT}")
        return

    with INPUT.open(newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = list(reader.fieldnames) if reader.fieldnames else []

        # Find the abstract column name (case-insensitive)
        abstract_col = None
        for col in fieldnames:
            if col and col.strip().lower() == 'abstract':
                abstract_col = col
                break

        if abstract_col is None:
            print("No 'Abstract' column found in input CSV. Available columns:")
            print(fieldnames)
            return

        out_fieldnames = fieldnames + ['word_count']

        rows = []
        for row in reader:
            abstract = row.get(abstract_col, '')
            wc = count_words(abstract)
            row['word_count'] = str(wc)
            rows.append(row)

    with OUTPUT.open('w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=out_fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Processed {len(rows)} rows. Output written to: {OUTPUT}")


if __name__ == '__main__':
    main()
