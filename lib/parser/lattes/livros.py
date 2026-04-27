import json
from pathlib import Path
import re
import os

from bs4 import BeautifulSoup
from groq import Groq
from dotenv import load_dotenv

from lib.helpers.normalize_autor import normalize_autor

load_dotenv()

api_key = os.getenv('GROQ_KEY')


def extrai_livros(id_lattes):
    
    arquivo = Path(f"/home/inacio/orbis/data/curriculos/{id_lattes}/cv.html")
    texto = arquivo.read_text(encoding="utf-8", errors="ignore")
    inicio = texto.find("Livros publicados/organizados ou edições")
    fim = texto.find("Capítulos de livros publicados", inicio)
    secao_livros = texto[inicio:fim]
    padrao = re.compile(
        r'<div class="layout-cell layout-cell-11"><span class="transform">(.*?)</span></div>',
        re.S
    )
    livros = padrao.findall(secao_livros)
    
    return livros

def parser_livros(livros):
    refs = []
    for livro in livros:
        d_l = {}
        # soup = BeautifulSoup(livro, 'html.parser')
        doi = livro.find('a', class_='icone-doi')
        if doi:
            href = doi.attrs['href']
            d_l['doi'] = href
        ref = livro.text
        norm_ref = normalize_ref(ref)
        autores = norm_ref.get('autores')
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
            "content": f"Extraia os dados e retorne APENAS JSON com campos: autores (array), titulo, editora, cidade, ano, edicao, volume, paginas.\n\n{referencia}"
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)