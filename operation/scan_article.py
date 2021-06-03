# -*- encoding: utf-8 -*-
from json import loads, dumps
from time import sleep
from random import randint, uniform
from rich.progress import Progress


def scan_article(browser):
    articlePath = 'data/articles.json'
    with open(articlePath, 'r', encoding='utf-8') as f:
        articles = f.read()
    # print(articles)
    articles = loads(articles)
    while True:
        randIndex = randint(0, len(articles) - 1)
        if articles[randIndex]['type'] != 'tuwen':
            del articles[randIndex]
            continue
        else:
            break
    url = articles[randIndex]['url']
    browser.get('https://www.xuexi.cn/d184e7597cc0da16f5d9f182907f1200/9a3668c13f6e303932b5e0e100fc248b.html')
    sleep(round(uniform(1, 3), 2))
    browser.get(url)
    sleep(round(uniform(1, 5), 2))

    # 看文章随机65-75秒
    totalTime = randint(65, 75)
    print('--> 正在浏览：《' + articles[randIndex]['title'] + '》')
    with Progress() as progress:
        task = progress.add_task("--> [cyan]浏览进度：", total=totalTime)
        while not progress.finished:
            browser.execute_script(
                'window.scrollBy(' + str(randint(2, 9)) + ',' + str(randint(15, 31)) + ')')
            sleepTime = round(uniform(1, 5), 2)
            progress.update(task, advance=sleepTime)
            sleep(sleepTime)

    print()
    del articles[randIndex]
    with open(articlePath, 'w', encoding='utf-8') as f:
        f.write(dumps(articles, ensure_ascii=False, indent=4))

