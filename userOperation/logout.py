# -*- encoding: utf-8 -*-
from random import uniform
from time import sleep
from selenium.webdriver.common.by import By
from custom.xuexi_chrome import XuexiChrome


def logout(browser: XuexiChrome):
    browser.xuexi_get('https://www.xuexi.cn/')
    sleep(round(uniform(1, 2), 2))
    logout_btn = browser.find_element(by=By.CLASS_NAME, value='logged-link')
    logout_btn.click()
