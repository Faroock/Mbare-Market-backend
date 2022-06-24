import math
from krcg.vtes import VTES

VTES.load()

def todas_las_cartas(tipo='Library', page=1, page_size=15):
    lista = list(VTES.search(type=[tipo]))
    total = len(lista)
    hasta = (page_size * page) - 1
    desde = hasta - page_size + 1
    data = lista[desde:hasta]
    pagination = {'total': total, 'from': desde + 1, 'to': hasta + 1}
    if hasta < total:
        pagination['next'] = f'?type={tipo}&page={page+1}&page_size={page_size}'
    else:
        pagination['to'] = desde + total - desde
    if page > 1:
        pagination['prev'] = f'?type={tipo}&page={page-1}&page_size={page_size}'
    if hasta >= total:
        del pagination['from']
        del pagination['to']
        pagination['prev'] = f'?type={tipo}&page={math.ceil(total/page_size)}&page_size={page_size}'
        pagination['error'] = 'Data overflow'
    return {'pagination': pagination, 'data': data}