import random
import time
from selenium import webdriver


def logout(browser):
    browser.get('https://www.xuexi.cn/')
    time.sleep(round(random.uniform(1, 2), 2))
    logoutBtn = browser.find_element_by_xpath('//*[@id="root"]/div/header/div[2]/div[2]/span/a')
    logoutBtn.click()


if __name__ == '__main__':
    browser = webdriver.Chrome()
    logout(browser)
