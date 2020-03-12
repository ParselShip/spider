# -*- encoding: utf-8  -*-
import requests
import concurrent.futures
import time


class HuYaSpider:
    def __init__(self, url):
        self.url = url
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

    def get_html_1(self):
        response = requests.get(self.url, headers=self.header)
        return response.json()

    def get_html_2(self, data):
        html = data['data']['datas']
        for img_html in html:
            name = img_html['nick']
            image_html = img_html['screenshot']
            res_img = requests.get(image_html, headers=self.header).content
            yield name, res_img

    def parse_html(self, data):
        with open(f'{data[0]}.jpg', mode='wb') as f:
            f.write(data[1])


def main():
    for i in range(1, 11):
        url = f'https://www.huya.com/cache.php?m=LiveList&do=getLiveListByPage&gameId=1663&tagAll=0&page={i}'
        hy = HuYaSpider(url)
        json_data = hy.get_html_1()
        data = hy.get_html_2(json_data)
        for i in data:
            hy.parse_html(i)


if __name__ == '__main__':
    start_time = time.time()
    execute = concurrent.futures.ThreadPoolExecutor(max_workers=100)
    execute.submit(main)
    execute.shutdown()
    # main()
    print('time:', start_time - time.time(), 's')
