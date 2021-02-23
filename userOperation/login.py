from selenium import webdriver
import time
import json


def add_cookie_login(browser):
    """
    自动登录流程，读取cookie文件，添加cookie，并尝试登录
    :param browser: browser
    :return: bool，表示是否登录成功
    """
    print('--> 尝试自动登陆')
    with open('data/cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        if cookie['name'] != 'token':
            continue
        browser.add_cookie({
            'domain': cookie['domain'],
            'name': cookie['name'],
            'value': cookie['value'],
            'path': cookie['path'],
            'secure': cookie['secure'],
            'httpOnly': cookie['httpOnly']
        })
    browser.get('https://pc.xuexi.cn/points/my-points.html')
    browser.implicitly_wait(5)
    time.sleep(1)
    if browser.current_url == 'https://pc.xuexi.cn/points/my-points.html':
        print('--> 自动登录成功')
        jsonCookies = json.dumps(browser.get_cookies())
        with open('data/cookies.json', 'w') as f:
            f.write(jsonCookies)
        return True
    print('--> 自动登录失败，准备扫码登录')
    return False


def normal_login(browser):
    """
    正常扫码登录流程
    :param browser: browser
    :return: bool，表示是否登录成功
    """
    print('--> 请在5分钟内扫码完成登录')
    browser.implicitly_wait(10)
    iframe = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/div/iframe')
    browser.switch_to.frame(iframe)
    login_QR_box = browser.find_element_by_xpath('/html/body/div/div/div[1]')
    browser.execute_script('arguments[0].scrollIntoView();', login_QR_box)

    for i in range(60):
        if browser.current_url == 'https://pc.xuexi.cn/points/my-points.html':
            print('--> 登录成功')
            jsonCookies = json.dumps(browser.get_cookies())
            with open('data/cookies.json', 'w') as f:
                f.write(jsonCookies)
            return True
        time.sleep(5)
    return False


def login(browser):
    """
    全部登录流程，将登录的最终结果返回给主程序
    :param browser: browser
    :return: bool，表示是否登录成功
    """
    browser.get('https://pc.xuexi.cn/points/my-points.html')
    time.sleep(2.5)
    settingsPath = 'data/settings.json'
    with open(settingsPath, 'r', encoding='utf-8') as f:
        settings = f.read()
    settings = json.loads(settings)
    if settings['保持登陆'] == "true":
        try:
            login_res = add_cookie_login(browser)
            if not login_res:
                login_res = normal_login(browser)
        except IOError:
            login_res = normal_login(browser)
    else:
        login_res = normal_login(browser)

    return login_res


if __name__ == '__main__':
    browser = webdriver.Chrome()
    login(browser)
