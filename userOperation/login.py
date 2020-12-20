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
    # login_QR = browser.find_element_by_xpath('/html/body/div/div/div[1]/div/div[1]/div[1]/img')
    browser.execute_script('arguments[0].scrollIntoView();', login_QR_box)
    # browser.switch_to_default_content()
    # server_headers = {
    #     'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"
    # }
    # server_data = {
    #     'text': "学习强国登录",
    #     'desp': "请在5分钟内完成登录！ ![logo](" + login_QR.get_attribute('src') + ")"
    # }
    # res = requests.post("https://sc.ftqq.com/SCU110175T0ad6cfa81c5ebb14bb3350eed3f7c4235f3f113d42803.send", headers=server_headers, data=server_data)
    # print('二维码获取成功')

    # 二维码有效时间5分钟
    # time.sleep(5*60)

    for i in range(60):
        if browser.current_url == 'https://pc.xuexi.cn/points/my-points.html':
            print('--> 登录成功')
            return True
        time.sleep(5)
    return False


if __name__ == '__main__':
    browser = webdriver.Chrome()
    login(browser)
