import unicodedata
import re

from lib.helpers.similarity.jaro import jaro_winkler


STOPWORDS = {'de', 'da', 'do', 'dos', 'das', 'e', 'von', 'van', 'del', 'di'}

def normalize(name: str) -> str:
    name = name.lower()
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    tokens = name.split()
    tokens = [t for t in tokens if re.sub(r'[^a-z]', '', t) not in STOPWORDS]
    name = ' '.join(tokens)
    name = re.sub(r'[^a-z\s]', '', name)
    return re.sub(r'\s+', ' ', name).strip()

def tokenize(name: str) -> list[str]:
    return normalize(name).split()

def token_set_ratio(t1: list[str], t2: list[str]) -> float:
    s1, s2 = set(t1), set(t2)
    inter = s1 & s2
    union = s1 | s2
    return len(inter) / len(union) if union else 0.0

def best_token_match(t1: list[str], t2: list[str]) -> float:
    if not t1 or not t2:
        return 0.0
    total = 0.0
    for a in t1:
        best = max(jaro_winkler(a, b) for b in t2)
        total += best
    return total / max(len(t1), len(t2))

def first_last_bonus(t1: list[str], t2: list[str]) -> float:
    if not t1 or not t2:
        return 0.0
    first = jaro_winkler(t1[0], t2[0])
    last  = jaro_winkler(t1[-1], t2[-1])
    return (first + last) / 2

def abbreviation_bonus(t1: list[str], t2: list[str]) -> float:
    bonus = 0.0
    for a in t1:
        for b in t2:
            if len(a) == 1 and b.startswith(a):
                bonus += 0.1
            elif len(b) == 1 and a.startswith(b):
                bonus += 0.1
    return min(bonus, 0.15)