# -*- encoding: utf-8 -*-
from json import dumps
from subprocess import call
from traceback import format_exc
from getData import get_article, get_video
from operation import scan_article, watch_video, exam, get_chromedriver
from userOperation import login, check
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import randint


def article_or_video():
    """
    伪随机(在随机浏览文章或视频的情况下，保证文章或视频不会连续2次以上重复出现)，浏览文章或视频
    :return: 1(文章)或2(视频)
    """
    rand = randint(1, 2)
    if len(randArr) >= 2 and randArr[len(randArr) - 1] + randArr[len(randArr) - 2] == 2:
        rand = 2
    elif len(randArr) >= 2 and randArr[len(randArr) - 1] + randArr[len(randArr) - 2] == 4:
        rand = 1
    randArr.append(rand)
    return rand


def user_login():
    """
    登录，循环执行，直到登录成功
    :return:
    """
    while not login.login(browser):
        print('--> 登录超时，正在尝试重新登录')
        continue


def run():
    """
    刷视频，刷题目主要部分
    通过check_task()函数决定应该执行什么任务，并调用相应任务函数
    :return: null
    """
    while True:
        checkRes = check.check_task(browser)
        if checkRes == check.CheckResType.NULL:
            break
        elif checkRes == check.CheckResType.ARTICLE:
            scan_article.scan_article(browser)
        elif checkRes == check.CheckResType.VIDEO:
            watch_video.watch_video(browser)
        elif checkRes == check.CheckResType.ARTICLE_AND_VIDEO:
            if article_or_video() == 1:
                scan_article.scan_article(browser)
            else:
                watch_video.watch_video(browser)
        else:
            exam.to_exam(browser, checkRes)


def finally_run():
    """
    程序最后执行的函数，包括打印信息、关闭浏览器等
    """
    browser.quit()

    print(r'''
      __/\\\\\\\\\\\\\____/\\\________/\\\__________/\\\\\\\\\\\\__/\\\\\\\\\\\\_____/\\\\\\\\\\\\\\\_        
       _\/\\\/////////\\\_\///\\\____/\\\/_________/\\\//////////__\/\\\////////\\\__\/\\\///////////__       
        _\/\\\_______\/\\\___\///\\\/\\\/__________/\\\_____________\/\\\______\//\\\_\/\\\_____________      
         _\/\\\\\\\\\\\\\\______\///\\\/___________\/\\\____/\\\\\\\_\/\\\_______\/\\\_\/\\\\\\\\\\\_____     
          _\/\\\/////////\\\_______\/\\\____________\/\\\___\/////\\\_\/\\\_______\/\\\_\/\\\///////______    
           _\/\\\_______\/\\\_______\/\\\____________\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_____________   
            _\/\\\_______\/\\\_______\/\\\____________\/\\\_______\/\\\_\/\\\_______/\\\__\/\\\_____________  
             _\/\\\\\\\\\\\\\/________\/\\\____________\//\\\\\\\\\\\\/__\/\\\\\\\\\\\\/___\/\\\_____________ 
              _\/////////////__________\///______________\////////////____\////////////_____\///______________ 
            ''')
    call('pause', shell=True)


if __name__ == "__main__":
    import os
    if not get_chromedriver.do(os.getcwd()):
        import sys
        sys.exit(1)

    chrome_options = Options()
    # 防止检测
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    chrome_options.add_argument("--mute-audio")  # 静音
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
    chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    chrome_options.add_argument('--ignore-ssl-errors')  # 忽略ssl错误
    chrome_options.add_argument('–log-level=3')

    browser = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver.exe'), options=chrome_options)
    browser.maximize_window()

    exam_temp_Path = './data/exam_temp.json'
    try:
        with open(exam_temp_Path, 'w', encoding='utf-8') as f:
            dataDict = {
                'DAILY_EXAM': 'true',
                'WEEKLY_EXAM': 'true',
                'SPECIAL_EXAM': 'true'
            }
            f.write(dumps(dataDict, ensure_ascii=False, indent=4))

        get_article.get_article()
        get_video.get_video()
        user_login()
        randArr = []  # 存放并用于判断随机值，防止出现连续看文章或者看视频的情况
        run()
        print('--> 任务全部完成，程序已结束')
    except:
        print(str(format_exc()))
        print('--> 程序异常，请尝试重启脚本')
    finally:
        os.remove(exam_temp_Path)
        finally_run()
