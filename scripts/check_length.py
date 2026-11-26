#!/usr/bin/env python3
"""Compare two voiceover scripts using words or Chinese characters."""
import argparse
import re
import sys
from pathlib import Path


def count_words(text):
    return len(re.findall(r"\b[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*\b", text))


def count_characters(text):
    return len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaffA-Za-z0-9]", text))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path, help="UTF-8 file containing only the original voiceover")
    parser.add_argument("rewrite", type=Path, help="UTF-8 file containing only the rewritten voiceover")
    parser.add_argument("--unit", choices=("words", "characters"), default="words")
    args = parser.parse_args()
    count = count_words if args.unit == "words" else count_characters
    original = count(args.original.read_text(encoding="utf-8"))
    rewrite = count(args.rewrite.read_text(encoding="utf-8"))
    if not original:
        print("Original voiceover contains no countable words or characters.", file=sys.stderr)
        return 2
    passed = rewrite * 10 < original * 11
    print(f"original={original} rewrite={rewrite} unit={args.unit} ratio={rewrite/original*100:.2f}% pass={str(passed).lower()}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
