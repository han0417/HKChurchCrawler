import requests as rq
import re
import json


def get_HK_coordinate(addr):
    addr_re = re.search(
        r'.+號', addr) or re.search(r'.+', addr)

    addr_re = addr_re.group() if addr_re != None else addr

    web = 'https://geocode.search.hereapi.com/v1/geocode?apiKey=xr73IahSek3LB4r41JszacgkHpkunu_0nuRSuXPVoBY&q='+addr_re

    content = rq.get(web)
    json_text = json.loads(content.text)
    if json_text['items'] == []:
        lat = ''
        log = ''
    else:
        lat = json_text['items'][0]['position']['lat']
        log = json_text['items'][0]['position']['lng']

    return [lat, log]
