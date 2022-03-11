# -*- encoding: utf-8 -*-
from time import sleep
from selenium.webdriver.common.by import By
from custom.xuexi_chrome import XuexiChrome


def login(browser: XuexiChrome):
    """
    扫码登录流程，将登录的最终结果返回给主程序
    :param browser: browser
    :return: bool，表示是否登录成功
    """
    browser.xuexi_get('https://pc.xuexi.cn/points/my-points.html')
    sleep(2.5)
    print('--> 请在5分钟内扫码完成登录')
    browser.implicitly_wait(10)
    qglogin = browser.find_element(by=By.ID, value='qglogin')
    browser.execute_script('arguments[0].scrollIntoView();', qglogin)

    for i in range(60):
        if browser.current_url == 'https://pc.xuexi.cn/points/my-points.html':
            print('--> 登录成功')
            return True
        sleep(5)
    return False
