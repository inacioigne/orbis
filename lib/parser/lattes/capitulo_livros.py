import os
import json
from groq import Groq
from dotenv import load_dotenv

from lib.helpers.normalize_autor import normalize_autor

load_dotenv()

api_key = os.getenv('GROQ_KEY')

def parser_capitulos(livros):
    
    refs = []
    for livro in livros:
        d_l = {}
        doi = livro.find('a', class_='icone-doi')
        if doi:
            href = doi.attrs['href']
            d_l['doi'] = href
        ref = livro.text
        norm_ref = normalize_ref(ref)
        autores = norm_ref.get('autores')
        if autores:
            n_autores = [normalize_autor(autor) for autor in autores]
            norm_ref['autores'] = n_autores
        d_l.update(norm_ref)
        refs.append(d_l)
        
    return refs


def normalize_ref(referencia):
    
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"Extraia os dados dessa referencia de capitulo de livro e retorne APENAS JSON com campos: autores (array), titulo-do-capitulo, titulo-do-livro, editora, cidade, ano, edicao, volume, page_start, page_end.\n\n{referencia}"
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)