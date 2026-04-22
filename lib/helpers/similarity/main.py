from lib.helpers.similarity.helpers import abbreviation_bonus, best_token_match, first_last_bonus, normalize, token_set_ratio, tokenize
from lib.helpers.similarity.jaro import jaro_winkler
from lib.helpers.similarity.levenshtein import edit_similarity


def check_similarity(name1: str, name2: str) -> dict:
    n1, n2 = normalize(name1), normalize(name2)
    t1, t2 = tokenize(name1), tokenize(name2)

    components = {
        'jaro_winkler':    (jaro_winkler(n1, n2),   0.20),
        'edit_similarity': (edit_similarity(n1, n2), 0.15),
        'token_set_ratio': (token_set_ratio(t1, t2), 0.20),
        'best_token_match':(best_token_match(t1, t2),0.25),
        'first_last_bonus':(first_last_bonus(t1, t2),0.20),
    }

    score = sum(v * w for v, w in components.values())
    score += abbreviation_bonus(t1, t2)
    score = min(1.0, score)

    if score >= 0.85:
        verdict = 'duplicate'
    elif score >= 0.65:
        verdict = 'review'
    else:
        verdict = 'distinct'

    return {
        'score': round(score, 4),
        'verdict': verdict,
        'components': {k: round(v, 4) for k, (v, _) in components.items()},
    }