from datetime import datetime
import re

from bs4 import BeautifulSoup

def get_update_lattes(html):
    soup = BeautifulSoup(html, "html.parser")
    informacoes_autor = soup.find('ul', class_='informacoes-autor')
    li = informacoes_autor.find_all('li')[-1]
    text = li.text
    pattern = r'(\d{2}/\d{2}/\d{4})'
    match = re.search(pattern, text)
    if match: 
        update = match.group(1)
        date = datetime.strptime(update, '%d/%m/%Y').date()
        return date
    else:
        return None