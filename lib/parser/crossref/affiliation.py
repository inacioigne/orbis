from lib.helpers.cleanText import clean_text


def get_affiliation(item):
    
    aff = item.get("affiliation")
    if isinstance(aff, list):
        if len(aff) == 0:
            return None
        
        affiliations = []
        for a in aff:
            name = clean_text(a.get("name"))
            if name:
                affiliations.append(name)
        raw_affiliation = " | ".join(affiliations)
        return raw_affiliation if raw_affiliation else None
    return None