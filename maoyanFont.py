# -*- coding: UTF-8 -*-
import parsel
import pytesseract
import requests
import re
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'
}


def get_html(url):
    response = requests.get(url, headers=headers)
    return response


def get_font():
    maoyan_html = get_html('https://maoyan.com/films/1190122')
    print(maoyan_html.url)
    pattern = re.compile("url\('(//vfile.meituan.net/colorstone/.*?.woff)'\) format\('woff'\);")
    print(pattern.findall(maoyan_html.text))
    font_url = 'http:' + pattern.findall(maoyan_html.text)[0]
    file_name = font_url.split('/')[-1]
    font_response = get_html(font_url)
    with open(file_name, mode='wb') as f:
        f.write(font_response.content)
    return file_name, maoyan_html.text


def get_map_font(file_name):
    font = TTFont(file_name)
    # 获取字体的编码
    font.saveXML('font.xml')
    code_list = font.getGlyphOrder()[2:]
    # 新建一张图片
    im = Image.new("RGB", (1800, 1800), (255, 255, 255))
    image_draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(file_name, 40)
    print(code_list)
    new_list = [code.replace('uni', '\\u') for code in code_list]
    print('替换之后', new_list)
    text = ''.join(new_list)
    # print(text)
    text = text.encode('utf-8').decode('unicode_escape')
    # print(text)
    image_draw.text((0, 100), text, font=font, fill="#000000")
    im.save("sss.jpg")
    im = Image.open("sss.jpg")
    res = pytesseract.image_to_string(im, lang="chi_sim")
    # print(res)
    res_str = [i for i in res]
    print(res_str)
    html_code_list = [i.lower().replace("uni", "&#x") + ";" for i in code_list]
    print(html_code_list)
    result = dict(zip(html_code_list, res_str))
    print(result)
    return result


def replace(html, pattern):
    # new_html = html
    for k, v in pattern.items():
        html = html.replace(k, v)
        print(k, v)
    with open('替换后.html', mode='w', encoding='utf-8') as f:
        f.write(html)
    return html


def parser(html):
    selector = parsel.Selector(html)
    aim = selector.css(".index-left .stonefont::text").getall()
    return aim


if __name__ == '__main__':
    filename = get_font()
    a = get_map_font(filename[0])
    htm = replace(filename[1], a)
    print(parser(htm))
