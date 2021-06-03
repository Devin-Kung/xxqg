# -*- encoding: utf-8 -*-
from getData import dataTimeOperation
from requests import get
from json import loads, dumps


def get_video():
    if not dataTimeOperation.is_get_data('videos'):
        return
    headers = {
        "Accept": "application/json",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "www.xuexi.cn",
        "Referer": "https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/b87d700beee2c44826a9202c75d18c85.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    articles = get(url='https://www.xuexi.cn/lgdata/4d82ahlubmol.json', headers=headers)
    with open('./data/videos.json', 'w', encoding='utf-8') as f:
        f.write(dumps(loads(articles.content), ensure_ascii=False, indent=4))
    dataTimeOperation.set_time('videos')
    print('--> 视频数据更新成功')


if __name__ == '__main__':
    get_video()
