from datetime import date, datetime
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GROQ_KEY')

def normalize_text_news(ref):
    meses = {
    "jan.": "01",
    "fev.": "02",
    "mar.": "03",
    "abr.": "04",
    "maio": "05",
    "jun.": "06",
    "jul.": "07",
    "ago.": "08",
    "set.": "09",
    "out.": "10",
    "nov.": "11",
    "dez.": "12"
    }

    data = ref.get('data')
    if data:
        if "/" in data:
            data = datetime.strptime(data, "%d/%m/%Y").date()
        else:
            partes = data.split()
            dia = partes[0]
            mes = meses[partes[1]]
            ano = partes[2]
            data = datetime.strptime(f"{dia}/{mes}/{ano}", "%d/%m/%Y").date()
        
        
    d_n = {
        'publication_type': 'text_news',
        'title': ref.get('titulo'),
        'date_published': data
        
    }
    return d_n


def normalize_ref_news(referencia):
    
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"Extraia os dados dessa referencia de textos em jornais e revistas e retorne APENAS JSON com campos: autores (array), titulo, titulo-da-revista, cidade, data.\n\n{referencia}"
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)