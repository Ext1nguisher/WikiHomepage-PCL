import requests
import re
from bs4 import BeautifulSoup


response = requests.get("https://zh.minecraft.wiki").text
obj = BeautifulSoup(response, 'html.parser')


def while_delete(del_txt, txt):
    while del_txt in txt:
        txt.remove(del_txt)
def gr():
    orgin = obj.find('div', class_="weekly-content").text
    return orgin.strip().split("。")


def gs():
    img_src = 'https://zh.minecraft.wiki' + obj.find('div', class_='weekly-image').find('img')['src']
    return img_src


print(gr())
