# -*- encoding: utf-8 -*-
import subprocess
from getData import get_article
from getData import get_video
from operation import scan_article
from operation import watch_video
from operation import exam
from userOperation import login
from userOperation import check
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random


def article_or_video():
    """
    伪随机，浏览文章或视频
    :return: 1(文章)或2(视频)
    """
    rand = random.randint(1, 2)
    if len(randArr) >= 2 and randArr[len(randArr) - 1] + randArr[len(randArr) - 2] == 2:
        rand = 2
    elif len(randArr) >= 2 and randArr[len(randArr) - 1] + randArr[len(randArr) - 2] == 4:
        rand = 1
    randArr.append(rand)
    return rand


def user_login():
    while not login.login(browser):
        print('--> 登录超时，已重新获取登录二维码')
        continue


def run():
    """
    刷视频，刷题目主要部分
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
    subprocess.call('pause', shell=True)


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")  # 静音
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
    chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    chrome_options.add_argument('--ignore-ssl-errors')  # 忽略ssl错误
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()

    try:
        get_article.get_article()
        get_video.get_video()
        user_login()
        randArr = []  # 存放并用于判断随机值，防止出现连续看文章或者看视频的情况
        run()
        print('--> 任务全部完成，程序已结束')
    except BaseException as e:
        print(e)
        print('--> 程序异常，请尝试重启脚本')
    finally:
        finally_run()
