# -*- encoding: utf-8 -*-
from json import loads
from enum import Enum
from rich import print
from rich.table import Table
from datetime import datetime
from custom.xuexi_chrome import XuexiChrome


class CheckResType(Enum):
    NULL = 0
    ARTICLE = 1
    VIDEO = 2
    ARTICLE_AND_VIDEO = 3
    DAILY_EXAM = 4
    WEEKLY_EXAM = 5
    SPECIAL_EXAM = 6


def check_task(browser: XuexiChrome):
    """
    检查任务项并返回给主程序
    :param browser: browser
    :return: CheckResType：任务类型
    """
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
    settings = loads(settings)

    exam_temp_Path = './data/exam_temp.json'
    with open(exam_temp_Path, 'r', encoding='utf-8') as f:
        exam_temp = f.read()
    exam_temp = loads(exam_temp)

    res = CheckResType.NULL
    browser.xuexi_get('https://www.xuexi.cn/index.html')
    browser.xuexi_get('https://pc.xuexi.cn/points/my-points.html')

    # 获取各任务项积分
    scores = browser.find_elements_by_class_name('my-points-card-text')
    for score in scores:
        tableRow.append(score.text.strip())

    # 今日积分
    todayPoints = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[2]/span[3]')
    tableRow.append(todayPoints.text.strip())
    # 总积分
    allPoints = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[2]/span[1]')
    tableRow.append(allPoints.text.strip())

    # 打印表格
    table.add_row(tableRow[0],
                  tableRow[1],
                  tableRow[2],
                  tableRow[3],
                  tableRow[4],
                  tableRow[5],
                  tableRow[6],
                  tableRow[7] + '分',
                  tableRow[8] + '分')
    print(table)

    if settings['浏览文章'] == "true" and scores[1].text != '12分/12分':
        res = CheckResType.ARTICLE
    if settings['观看视频'] == "true" and (scores[2].text != '6分/6分' or scores[3].text != '6分/6分'):
        if res == CheckResType.ARTICLE:
            res = CheckResType.ARTICLE_AND_VIDEO
        else:
            res = CheckResType.VIDEO

    # 检查设置文件
    if settings['自动答题'] != 'true':
        return res

    dayOfWeek = str(datetime.now().isoweekday())
    if settings['每日答题'] == 'true' and res == CheckResType.NULL and scores[4].text != '5分/5分':
        if settings['答题时间设置']['是否启用(关闭则每天都答题)'] != 'true' or (settings['答题时间设置']['是否启用(关闭则每天都答题)'] == 'true' and dayOfWeek in settings['答题时间设置']['答题类型(数字代表星期几)']['每日答题']):
            res = CheckResType.DAILY_EXAM
    if exam_temp['WEEKLY_EXAM'] == 'true' and settings['每周答题'] == 'true' and res == CheckResType.NULL and scores[5].text != '5分/5分':
        if settings['答题时间设置']['是否启用(关闭则每天都答题)'] != 'true' or (settings['答题时间设置']['是否启用(关闭则每天都答题)'] == 'true' and dayOfWeek in settings['答题时间设置']['答题类型(数字代表星期几)']['每周答题']):
            res = CheckResType.WEEKLY_EXAM
    if exam_temp['SPECIAL_EXAM'] == 'true' and settings['专项答题'] == 'true' and res == CheckResType.NULL and scores[6].text != '10分/10分':
        if settings['答题时间设置']['是否启用(关闭则每天都答题)'] != 'true' or (settings['答题时间设置']['是否启用(关闭则每天都答题)'] == 'true' and dayOfWeek in settings['答题时间设置']['答题类型(数字代表星期几)']['专项答题']):
            res = CheckResType.SPECIAL_EXAM

    return res
