# -*- encoding: utf-8 -*-
from json import loads, dumps
from time import sleep
from random import randint, uniform
from rich.progress import Progress
from custom.xuexi_chrome import XuexiChrome


def scan_article(browser: XuexiChrome):
    article_path = 'data/articles.json'
    with open(article_path, 'r', encoding='utf-8') as f:
        articles = f.read()
    # print(articles)
    articles = loads(articles)
    while True:
        rand_index = randint(0, len(articles) - 1)
        if articles[rand_index]['type'] != 'tuwen':
            del articles[rand_index]
            continue
        else:
            break
    url = articles[rand_index]['url']
    browser.xuexi_get('https://www.xuexi.cn/d184e7597cc0da16f5d9f182907f1200/9a3668c13f6e303932b5e0e100fc248b.html')
    browser.xuexi_get(url)

    # 看文章随机70-75秒
    total_time = randint(70, 75)
    print('--> 正在浏览：《' + articles[rand_index]['title'] + '》')
    with Progress() as progress:
        task = progress.add_task("--> [cyan]浏览进度：", total=total_time)
        while not progress.finished:
            browser.execute_script(
                'window.scrollBy(' + str(randint(2, 9)) + ',' + str(randint(15, 31)) + ')')
            sleep_time = round(uniform(1, 5), 2)
            progress.update(task, advance=sleep_time)
            sleep(sleep_time)

    print()
    del articles[rand_index]
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(dumps(articles, ensure_ascii=False, indent=4))

