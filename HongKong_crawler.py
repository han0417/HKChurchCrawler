from bs4 import BeautifulSoup as bs
from HK_coordinate import get_HK_coordinate

import requests as rq
import re
import pymysql
import json
import time


class HongKong():

    web = 'https://catholic.org.hk/%e5%85%a8%e6%b8%af%e5%bd%8c%e6%92%92%e6%99%82%e9%96%93/'
    content = rq.get(web)
    soup = bs(content.text, "lxml")
    church_contents = soup.select(".su-spoiler-content")
    # all_data = []
    for item in church_contents:
        # arr = {}
        # 教堂名稱
        name_text = re.search(
            r'[\w]+[^堂向禮]堂', item.text) or re.search(r'.+中心', item.text) or re.search(r'.+書院', item.text)
        if name_text.group() == "彌撒中心":
            name_text = "地利亞英文小學暨幼稚園"+name_text.group()
        elif name_text.group() == "平日彌撒及明供聖體仍舊在聖堂":
            name_text = "聖芳濟各書院"
        elif name_text.group() == "聖瑪竇宗徒堂":
            name_text = "聖瑪竇宗徒彌撒中心"
        else:
            name_text = name_text.group()

        # 教堂電話
        phone_text = re.search(r'(?<=電話：).+', item.text)

        if (phone_text is None):
            phone_text = None
        else:
            phone_text = phone_text.group()

        # # 教堂地址
        address_text = re.search(
            r'香港.+', item.text) or re.search(r'九龍.+', item.text) or re.search(r'新界.+', item.text) or re.search(r'大嶼山.+', item.text) or re.search(r'愉景灣.+', item.text)
        if address_text.group() == "香港中文大學":
            address_text = "新界沙田香港中文大學"
        else:
            address_text = address_text.group()

        priest_text = re.search(
            r'[\w\u3000]+(?=（主任司鐸）)', item.text) or re.search(r'(?<=委員會會長：).+', item.text) or re.search(r'(?<=署理主任司鐸：).+', item.text) or re.search(r'[\w]+(?=（負責人）)', item.text) or re.search(r'[\w]+神父', item.text)
        if priest_text is None:
            priest_text = None

        else:
            priest_text = priest_text.group().replace("\u3000", "")

        # 彌撒時間
        mass_text = re.search(
            r'(?<=主日彌撒：).+', item.text) or re.search(r'(?<=彌撒：).+', item.text) or re.search(r'(?<=[^提前]主日彌撒).+', item.text)
        if name_text == "聖母聖衣堂":
            mass_text = "中文 | 8:30am, 10:00am 英文 | 11:00am*, 11:45am, 6:00pm"
        elif name_text == "教區傷殘人士牧民中心":
            mass_text = "首主日中午十二時（特為傷殘人士）。首主日下午五時（特為聽障人士，設手語翻譯）。第二個星期六晚上八時（主日提前彌撒）（特為聽障人士，設手語翻譯）。第三個星期日下午五時（粵語）"
        elif (mass_text is None):
            mass_text = None
        else:
            mass_text = mass_text.group()

        data = {
            'name': name_text,
            'address': address_text,
            'phone': phone_text,
            'priest': priest_text,
            'other': None,
            'mass': mass_text,
            'url': web,
            'img': None,
            'parish': '香港教區',
            'deanery': "無",
            'country': '香港',
        }

        coordinate = get_HK_coordinate(data['address'])
        latitude = coordinate[0]
        longitude = coordinate[1]
        print(data['name'], data['address'], latitude, longitude)
        time.sleep(1)
