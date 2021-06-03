# -*- encoding: utf-8 -*-
from time import sleep


def login(browser):
    """
    扫码登录流程，将登录的最终结果返回给主程序
    :param browser: browser
    :return: bool，表示是否登录成功
    """
    browser.get('https://pc.xuexi.cn/points/my-points.html')
    sleep(2.5)
    print('--> 请在5分钟内扫码完成登录')
    browser.implicitly_wait(10)
    iframe = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/div/iframe')
    browser.switch_to.frame(iframe)
    login_QR_box = browser.find_element_by_xpath('/html/body/div/div/div[1]')
    browser.execute_script('arguments[0].scrollIntoView();', login_QR_box)

    for i in range(60):
        if browser.current_url == 'https://pc.xuexi.cn/points/my-points.html':
            print('--> 登录成功')
            return True
        sleep(5)
    return False
