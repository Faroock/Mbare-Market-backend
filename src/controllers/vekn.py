import requests
from bs4 import BeautifulSoup

def get_usuario_from_vekn(vekn_id: int):
    contenido = {"vekn_id": vekn_id}
    try:
        vekn_url = f'https://www.vekn.net/player-registry/player/{vekn_id}'
        resp = requests.get(vekn_url, headers={'Cache-Control': 'no-transform'})
        page = resp.text
        soup = BeautifulSoup(page, 'html.parser')
        alert = soup.find('div', class_='alert-message')
        if alert:
            contenido['message'] = alert.get_text()
            contenido['status'] = -1
        else:
            nombre = soup.find('div', class_='componentheading').get_text()
            contenido['name'] = nombre.split('(')[0].rstrip()
            tabla = soup.find('table', class_='contentpaneopen')
            rows = tabla.find_all('tr')
            for row in rows:
                key = row.find('th').get_text()
                value = row.find('td').get_text()
                if key:
                    contenido[key.lower()] = value if value != "" else None
            contenido['status'] = 0
    finally:
        return contenido