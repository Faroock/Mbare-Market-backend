import statistics
import requests
from requests.utils import requote_uri
from bs4 import BeautifulSoup

url_base = 'https://www.collectors.com/search?days=Any&lowprice=Any&highprice=Any&sellerexclude=false'
url_ebay = 'https://www.ebay.com/sch/i.html?LH_BIN=1'

def get_details_pices(card):
    page = requests.get(url_base + '&searchterm=' + requote_uri('VTES ' + card))
    soup = BeautifulSoup(page.content, "html.parser")
    list_cards = soup.find_all('div', class_='searchresultitem')
    ret = []
    for item in list_cards:
        prices = item.find('div', class_='itemsaleprice')
        detail = item.find('div', class_='itemdescr')
        if prices and detail:
            cant = get_quantity(detail.text)
            price = float(prices.text[6::])
            ret.append({'descr': detail.text, 'price': price, 'quantity': cant, 'unit': price/cant})
    return ret

def get_price(card):
    details = get_details_pices(card)
    if len(details) > 0:
        prices = [x['unit'] for x in details]
        desv = statistics.stdev(prices) if len(prices) > 1 else 0
        sum_price = 0
        for carta in details:
            sum_price += carta['unit']
        promedio = sum_price/len(details)
        if desv > promedio:
            precio = promedio + (desv / 2)
        else:
            precio = promedio + desv
        return {'carta': card, 'precio': round(precio, 2), 'promedio': promedio, 'desviacion': desv}
    else:
        return {'carta': card, 'precio': 'Preguntar por inbox'}

def get_quantity(descr):
    fst_sep = descr.replace('(','').replace(')','').split(' ')
    num = 1
    for word in fst_sep:
        if word[0:1:] == 'x':
            word = word[1::]
        try:
            num = int(word)
        except ValueError:
            pass
    return num

def _get_list_from_ebay(card, tipo=None):
    page = requests.get(url_ebay + '&_nkw=' + requote_uri('VTES ' + card + ' ' + tipo))
    soup = BeautifulSoup(page.content, "html.parser")
    list_cards = soup.find_all('div', class_='s-item__wrapper clearfix')
    for item in list_cards:
        title = item.find('a', class_='s-item__link')
        price = item.find('span', class_='s-item__price')
        print(title.text)
        if price:
            print(price.text)
        else:
            print('Sin precio')
    return list_cards
    

if __name__ == '__main__':
    pass