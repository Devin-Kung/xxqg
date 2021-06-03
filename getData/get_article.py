# -*- encoding: utf-8 -*-
from getData import dataTimeOperation
from requests import get
from json import loads, dumps


def get_article():
    if not dataTimeOperation.is_get_data('articles'):
        return
    headers = {
        "Accept": "application/json",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "www.xuexi.cn",
        "Referer": "https://www.xuexi.cn/4f5aa999a479568bf620109395d8fe56/69fe65d658afc891dd105e1ce9e5879d.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    articles = get(url='https://www.xuexi.cn/lgdata/u1ght1omn2.json', headers=headers)
    with open('./data/articles.json', 'w', encoding='utf-8') as f:
        f.write(dumps(loads(articles.content), ensure_ascii=False, indent=4))
    dataTimeOperation.set_time('articles')
    print('--> 文章数据更新成功')


if __name__ == '__main__':
    get_article()
