import requests
from selenium import webdriver
import time


def login(browser):
    browser.get('https://pc.xuexi.cn/points/my-points.html')
    print('--> 请在5分钟内完成登录')
    browser.implicitly_wait(10)
    iframe = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/div/iframe')
    browser.switch_to.frame(iframe)
    login_QR_box = browser.find_element_by_xpath('/html/body/div/div/div[1]')
    browser.execute_script('arguments[0].scrollIntoView();', login_QR_box)
    for i in range(60):
        if browser.current_url == 'https://pc.xuexi.cn/points/my-points.html':
            print('--> 登录成功')
            return True
        time.sleep(5)
    return False


if __name__ == '__main__':
    browser = webdriver.Chrome()
    login(browser)
