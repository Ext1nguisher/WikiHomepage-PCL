import requests
import re


def delete_by_start_and_end(string, start, end):
    """使用正则表达式,删除指定字符串两段文字之间的指定文字"""
    result = string[:]
    while start in result and end in result:
        result = re.sub(f'{start}.*?{end}', "", string)
    return result


def delete_text_directly(string, *texts):
    """使用正则表达式,删除指定字符串中的指定文字"""
    result = string[:]
    for text in texts:
        while text in result:
            result = re.sub(text, "", result)
    return result


def gr():
    response = requests.get("https://zh.minecraft.wiki").text
    obj = re.search(r'<div class="weekly-content">.*?</div>', response, re.S)
    text = response[obj.span()[0]:obj.span()[1]]
    text = delete_by_start_and_end(text, "<a", ">")
    text = delete_by_start_and_end(text, "<span", ">")
    text = delete_by_start_and_end(text, "<div", ">")
    text = delete_by_start_and_end(text, "<p", ">")
    text = re.sub(r'（', r'(', text)
    text = re.sub(r'）', r')', text)
    text = delete_by_start_and_end(text, "图为", "。")
    text = delete_text_directly(text,
                                "</a>", "</sub>", "<p>", "<b>", "</b>",
                                "<span>", "</span>", "</p>", "<sub>", "</sup>", "<sup>", "</div>")
    text = text.strip().split("\n")
    return text


def reload():
    with open("Custom.xaml", "r+", encoding="utf-8") as f:
        content = f.read()
        for i, t in enumerate(gr()):
            content = re.sub(f'<!-- {i} -->.*?<!-- end_{i} -->', f'<!-- {i} -->{t}<!-- end_{i} -->', content)

    with open("Custom.xaml", "w+", encoding="utf-8") as f:
        f.write(content)


reload()
