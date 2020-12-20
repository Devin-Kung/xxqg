from selenium import webdriver
import json
import time
import random
from rich.progress import Progress


def scan_article(browser):
    articlePath = 'data/articles.json'
    with open(articlePath, 'r', encoding='utf-8') as f:
        articles = f.read()
    # print(articles)
    articles = json.loads(articles)
    while True:
        randIndex = random.randint(0, len(articles) - 1)
        if articles[randIndex]['type'] != 'tuwen':
            del articles[randIndex]
            continue
        else:
            break
    url = articles[randIndex]['url']
    browser.get('https://www.xuexi.cn/d184e7597cc0da16f5d9f182907f1200/9a3668c13f6e303932b5e0e100fc248b.html')
    time.sleep(round(random.uniform(1, 3), 2))
    browser.get(url)
    time.sleep(round(random.uniform(1, 5), 2))

    # 看文章随机65-75秒
    totalTime = random.randint(65, 75)
    print('--> 正在浏览：《' + articles[randIndex]['title'] + '》')
    with Progress() as progress:
        task = progress.add_task("--> [cyan]浏览进度：", total=totalTime)
        while not progress.finished:
            browser.execute_script(
                'window.scrollBy(' + str(random.randint(2, 9)) + ',' + str(random.randint(15, 31)) + ')')
            sleepTime = round(random.uniform(1, 5), 2)
            progress.update(task, advance=sleepTime)
            time.sleep(sleepTime)

    print()
    del articles[randIndex]
    with open(articlePath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(articles, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    # # 实例化谷歌设置选项
    # option = webdriver.ChromeOptions()
    # # 添加保持登录的数据路径
    # option.add_argument(r"--user-data-dir=C:\Users\Raichu\AppData\Local\Google\Chrome\User Data")
    # browser = webdriver.Chrome(options=option)
    browser = webdriver.Chrome()
    scan_article(browser)
    browser.quit()
