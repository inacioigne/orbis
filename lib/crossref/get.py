import json

import httpx


def get_article_crossref(articles, id_lattes):
    
    error = []
    with open(f"data/curriculos/{id_lattes}/article_crossref.jsonl", "w", encoding="utf-8") as f:
        
        for i in articles:
            doi = i['doi'][0]
            url = f"https://api.crossref.org/v1/works/{doi}"
            r = httpx.get(url)
            print(r.status_code)
            if r.status_code == 200:
                item = r.json()['message']
                json.dump(item, f)
                f.write("\n")
            else:
                print(f"Error fetching data for DOI: {doi}, status code: {r.status_code}")
                error.append(i)
                
    return error