# feature_extraction.py
import re
from typing import List

def cleanup_line(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()

def extract_features(text: str) -> List[str]:
    # Lightweight, robust splitting: bullets, lines, sentences
    lines = re.split(r'(?:\r?\n|\.\s+|;|\u2022|-)', text)
    features = []
    seen = set()
    for l in lines:
        f = cleanup_line(l)
        if not f or len(f) < 6:
            continue
        # avoid capture of "1. Introduction" style
        if re.match(r'^\d+\W*$', f):
            continue
        key = f.lower()
        if key in seen:
            continue
        seen.add(key)
        features.append(f)
    return features
