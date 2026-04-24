def parser_container_lattes(article):
    
    [name] = article.get('nomePeriodico')
    [issn] = article.get('issn')
    
    return {
        'name': name,
        'issn_print': issn
    }