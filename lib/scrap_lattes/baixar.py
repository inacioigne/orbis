import time


def baixar_lattes(driver, lattes_id):
    if len(lattes_id) == 16:
        print(f'Baixando curriculo com ID: {lattes_id}')
        url = f'https://lattes.cnpq.br/{lattes_id}'
        driver.get(url)
        lid10 = driver.current_url.split('id=')[1]
        url_preview = f'http://buscatextual.cnpq.br/buscatextual/preview.do?metodo=apresentar&id={lid10}'
        driver.get(url_preview)
        time.sleep(3)
        cmd_open_cv = 'abreCV()'
        driver.execute_script(cmd_open_cv)
        time.sleep(3)
        window = driver.window_handles[-1]
        driver.switch_to.window(window)
        html = driver.page_source
        # with open('data/cv.html', 'w') as f:
        #     f.write(html)
        driver.quit()
        return html
    
    else:
        raise ValueError("O ID do Lattes deve conter exatamente 16 caracteres.")