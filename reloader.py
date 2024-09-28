import requests
import re
import datetime
from bs4 import BeautifulSoup

response = requests.get("https://zh.minecraft.wiki").text
obj = BeautifulSoup(response, 'html.parser')


def while_delete(del_txt, txt):
    while del_txt in txt:
        txt.remove(del_txt)


def gr():
    orgin = obj.find('div', class_="weekly-content").text
    return orgin.strip().split("。")


def get_link_txt(txt):
    raw_links = re.findall(r'<a href=".*?" title=', txt.decode(eventual_encoding='UTF-8'), re.S)
    links = []
    for l in raw_links:
        links.append("https://zh.minecraft.wiki" +
                     l[re.search(r'".*?"', l).span()[0]:re.search(r'".*?"', l).span()[1]].strip('"'))
    return links


def gs():
    img_src = 'https://zh.minecraft.wiki' + obj.find('div', class_='weekly-image').find('img')['src']
    return img_src


def update():
    now = datetime.datetime.now()
    with open("Custom.xaml", "r", encoding='UTF-8') as f:
        content_text = f.read()
    with open("Custom.xaml", "w", encoding='UTF-8') as f:
        txt = re.sub(
            r'<sys:String x:Key="imgLink">.*?</sys:String>',
            f'<sys:String x:Key="imgLink">{gs()}</sys:String>', content_text)
        txt = re.sub(r'<sys:String x:Key="datetime">.*?</sys:String>',
                     f'<sys:String x:Key="datetime">最后更新：{now.strftime("%Y-%m-%d")}</sys:String>', txt)
        print(txt)
        f.write(txt)


update()
