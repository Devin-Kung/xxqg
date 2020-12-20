import time
import random
import json
from enum import Enum
from selenium import webdriver
from rich import print
from rich.table import Column, Table


class CheckResType(Enum):
    NULL = 0
    ARTICLE = 1
    VIDEO = 2
    ARTICLE_AND_VIDEO = 3
    DAILY_EXAM = 4
    WEEKLY_EXAM = 5
    SPECIAL_EXAM = 6


def check_task(browser):
    # table = PrettyTable(["每日登录", "选读文章", "视频数量", "视频时长", "每日答题", "每周答题", "专项答题", "今日累计积分", "成长总积分"])
    table = Table(show_header=True, header_style="bold black")
    table.add_column("每日登录", justify='center')
    table.add_column("选读文章", justify='center')
    table.add_column("视频数量", justify='center')
    table.add_column("视频时长", justify='center')
    table.add_column("每日答题", justify='center')
    table.add_column("每周答题", justify='center')
    table.add_column("专项答题", justify='center')
    table.add_column("今日累计积分", justify='center')
    table.add_column("成长总积分", justify='center')
    tableRow = []
    settingsPath = 'data/settings.json'
    with open(settingsPath, 'r', encoding='utf-8') as f:
        settings = f.read()
    # print(settings)
    settings = json.loads(settings)

    res = CheckResType.NULL
    browser.get('https://www.xuexi.cn/index.html')
    time.sleep(round(random.uniform(1, 3), 2))
    browser.get('https://pc.xuexi.cn/points/my-points.html')
    browser.implicitly_wait(3)
    time.sleep(round(random.uniform(1, 3), 2))

    # 每日登录积分
    login = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]')
    tableRow.append(login.text)

    # 选读文章积分
    article = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div[2]')
    tableRow.append(article.text)
    if article.text != '12分/12分':
        res = CheckResType.ARTICLE

    # 视听学习积分
    video = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[3]/div[2]/div[3]/div[2]/div[1]/div[2]')
    tableRow.append(video.text)

    # 视听学习时长积分
    video_time = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[3]/div[2]/div[4]/div[2]/div[1]/div[2]')
    tableRow.append(video_time.text)
    if video.text != '6分/6分' or video_time.text != '6分/6分':
        if res == CheckResType.ARTICLE:
            res = CheckResType.ARTICLE_AND_VIDEO
        else:
            res = CheckResType.VIDEO

    # 检查设置文件
    if settings['自动答题'] != 'true':
        return res

    # 每日答题积分
    daily = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[1]/div[2]')
    tableRow.append(daily.text)
    if settings['每日答题'] == 'true':
        if res == CheckResType.NULL and daily.text != '5分/5分':
            res = CheckResType.DAILY_EXAM

    # 每周答题积分
    weekly = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[1]/div[2]')
    tableRow.append(weekly.text)
    if settings['每周答题'] == 'true':
        if res == CheckResType.NULL and weekly.text != '5分/5分':
            res = CheckResType.WEEKLY_EXAM

    # 专项答题积分
    special = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[7]/div[2]/div[1]/div[2]')
    tableRow.append(special.text)
    if settings['专项答题'] == 'true':
        if res == CheckResType.NULL and special.text != '10分/10分':
            res = CheckResType.SPECIAL_EXAM

    # 今日积分
    todayPoints = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[2]/span[3]')
    # 总积分
    allPoints = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[2]/span[1]')
    tableRow.append(todayPoints.text)
    tableRow.append(allPoints.text)
    table.add_row(tableRow[0], tableRow[1], tableRow[2], tableRow[3], tableRow[4], tableRow[5], tableRow[6], tableRow[7] + '分', tableRow[8] + '分')
    print(table)
    return res


