# -*- encoding: utf-8 -*-
from json import loads, dumps
from time import sleep
from random import randint, uniform
from rich.progress import Progress
from selenium.webdriver.common.by import By
from custom.xuexi_chrome import XuexiChrome


def watch_video(browser: XuexiChrome):
    video_path = 'data/videos.json'
    with open(video_path, 'r', encoding='utf-8') as f:
        videos = f.read()
    # print(videos)
    videos = loads(videos)
    while True:
        rand_index = randint(0, len(videos) - 1)
        if videos[rand_index]['type'] != 'shipin':
            del videos[rand_index]
            continue
        else:
            break

    url = videos[rand_index]['url']
    browser.xuexi_get('https://www.xuexi.cn/0809b8b6ab8a81a4f55ce9cbefa16eff/ae60b027cb83715fd0eeb7bb2527e88b.html')
    browser.xuexi_get('https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html#t1jk1cdl7l-5')
    browser.xuexi_get(url)
    video = browser.find_element(by=By.TAG_NAME, value='video')
    start = browser.find_element(by=By.CLASS_NAME, value='outter')
    sleep(round(uniform(1, 3), 2))
    browser.execute_script('arguments[0].scrollIntoView();', video)
    try:
        start.click()
    except BaseException:
        pass

    # 看视频随机70-75秒
    total_time = randint(70, 75)
    print('--> 正在观看：《' + videos[rand_index]['title'] + '》')
    with Progress() as progress:
        task = progress.add_task("--> [red]观看进度：", total=total_time)
        while not progress.finished:
            sleep_time = round(uniform(1, 3), 2)
            progress.update(task, advance=sleep_time)
            sleep(sleep_time)

    print()

    del videos[rand_index]
    with open(video_path, 'w', encoding='utf-8') as f:
        f.write(dumps(videos, ensure_ascii=False, indent=4))


