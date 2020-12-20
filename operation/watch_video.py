from selenium import webdriver
import json
import time
import random
from rich.progress import Progress


def watch_video(browser):
    videoPath = 'data/videos.json'
    with open(videoPath, 'r', encoding='utf-8') as f:
        videos = f.read()
    # print(videos)
    videos = json.loads(videos)
    while True:
        randIndex = random.randint(0, len(videos) - 1)
        if videos[randIndex]['type'] != 'shipin':
            del videos[randIndex]
            continue
        else:
            break

    url = videos[randIndex]['url']
    browser.get('https://www.xuexi.cn/0809b8b6ab8a81a4f55ce9cbefa16eff/ae60b027cb83715fd0eeb7bb2527e88b.html')
    time.sleep(round(random.uniform(1, 3), 2))
    browser.get('https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html#t1jk1cdl7l-5')
    time.sleep(round(random.uniform(1, 3), 2))
    browser.get(url)
    time.sleep(round(random.uniform(3, 6), 2))
    video = browser.find_element_by_xpath('/html/body/div/div/section/div/div/div/div/div[2]/section/div/div/div/div/div/div/div/div[1]/div[2]/div/div[1]/div[1]/div/video')
    start = browser.find_element_by_xpath(
        '/html/body/div/div/section/div/div/div/div/div[2]/section/div/div/div/div/div/div/div/div[1]/div[2]/div/div[1]/div[1]/div/div[1]')
    time.sleep(round(random.uniform(1, 3), 2))
    browser.execute_script('arguments[0].scrollIntoView();', video)
    try:
        start.click()
    except BaseException as e:
        pass

    # 看视频随机65-75秒
    totalTime = random.randint(65, 75)
    print('--> 正在观看：《' + videos[randIndex]['title'] + '》')
    with Progress() as progress:
        task = progress.add_task("--> [red]观看进度：", total=totalTime)
        while not progress.finished:
            sleepTime = round(random.uniform(1, 3), 2)
            progress.update(task, advance=sleepTime)
            time.sleep(sleepTime)

    print()

    del videos[randIndex]
    with open(videoPath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(videos, ensure_ascii=False, indent=4))


