# -*- encoding: utf-8 -*-
from json import loads, dumps
from traceback import format_exc
from selenium.common.exceptions import WebDriverException, NoSuchElementException, UnexpectedAlertPresentException
from time import sleep
from random import uniform
from difflib import SequenceMatcher
from re import findall
from selenium.webdriver.remote.webelement import WebElement
from custom.xuexi_chrome import XuexiChrome
from userOperation import check


def click(browser: XuexiChrome, element: WebElement):
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                window.alert = function() {
                    return;
                }
              '''
    })
    element.click()


def check_exam(browser, examType):
    """
    检查可做的题目，如果本页没有则翻页查找
    :param browser: browser
    :param examType: 题目类型(周、专)
    :return: null
    """
    sleep(round(uniform(1, 2), 2))
    while True:
        flag = True  # 用来记录是否答题，答题则置为False
        allExams = browser.find_elements_by_class_name('ant-btn-primary')
        for exam in allExams:
            if exam.text == '开始答题' or exam.text == '继续答题':
                browser.execute_script('arguments[0].scrollIntoView();', exam)
                sleep(round(uniform(1, 2), 2))
                click(browser, exam)
                sleep(round(uniform(2, 4), 2))
                run_exam(browser)
                flag = False
                break
        if flag:  # flag为True则执行翻页
            nextPage = browser.find_element_by_class_name('ant-pagination-next')
            browser.execute_script('arguments[0].scrollIntoView();', nextPage)
            sleep(round(uniform(1, 2), 2))
            if nextPage.get_attribute('aria-disabled') == 'true':  # 检查翻页按钮是否可点击
                exam_type = None
                if examType == check.CheckResType.WEEKLY_EXAM:
                    exam_type = 'WEEKLY_EXAM'
                    print('--> 每周答题：已无可做题目')
                elif examType == check.CheckResType.SPECIAL_EXAM:
                    exam_type = 'SPECIAL_EXAM'
                    print('--> 专项答题：已无可做题目')
                # 如果该类型的题目已全部做完，则记录防止再次刷
                exam_temp_Path = './data/exam_temp.json'
                with open(exam_temp_Path, 'r', encoding='utf-8') as f:
                    dataDict = loads(f.read())
                    dataDict[exam_type] = 'false'
                with open(exam_temp_Path, 'w', encoding='utf-8') as f:
                    f.write(dumps(dataDict, ensure_ascii=False, indent=4))
                return
            click(browser, nextPage)
            sleep(round(uniform(3, 5), 2))
        else:
            break


def to_exam(browser: XuexiChrome, examType: check.CheckResType):
    """
    根据参数题目类型进入对应的题目
    :param browser: browser
    :param examType: 题目类型(日、周、专)
    :return:
    """
    browser.xuexi_get('https://www.xuexi.cn/')
    browser.xuexi_get('https://pc.xuexi.cn/points/my-points.html')
    sleep(round(uniform(1, 2), 2))

    if examType == check.CheckResType.DAILY_EXAM:
        daily = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[2]/div')
        browser.execute_script('arguments[0].scrollIntoView();', daily)
        sleep(round(uniform(1, 2), 2))
        click(browser, daily)
        sleep(round(uniform(2, 4), 2))
        run_exam(browser)
    elif examType == check.CheckResType.WEEKLY_EXAM:
        weekly = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[2]/div')
        browser.execute_script('arguments[0].scrollIntoView();', weekly)
        sleep(round(uniform(1, 2), 2))
        click(browser, weekly)
        check_exam(browser, examType)
    elif examType == check.CheckResType.SPECIAL_EXAM:
        special = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[7]/div[2]/div[2]/div')
        browser.execute_script('arguments[0].scrollIntoView();', special)
        sleep(round(uniform(1, 2), 2))
        click(browser, special)
        check_exam(browser, examType)


def select_all(options):
    print('-->    最大概率选项：', end='')
    for i in range(len(options)):
        print(' ' + options[i].text[0], end='')
    print()
    for i in range(len(options)):
        sleep(round(uniform(0.2, 0.8), 2))
        options[i].click()


def run_exam(browser):
    while True:
        content = browser.find_element_by_class_name('ant-breadcrumb')
        browser.execute_script('arguments[0].scrollIntoView();', content)
        sleep(round(uniform(2, 3), 2))
        # 题目类型
        questionType = browser.find_element_by_class_name('q-header').text
        # print(questionType)
        # 当前题目的坐标
        questionIndex = int(browser.find_element_by_class_name('big').text)
        # 题目总数
        questionCount = int(findall('/(.*)', browser.find_element_by_class_name('pager').text)[0])
        # 确定按钮
        okBtn = browser.find_element_by_class_name('ant-btn-primary')
        try:
            browser.find_element_by_class_name('answer')
            if okBtn.text == '下一题':
                okBtn.click()
                sleep(round(uniform(0.2, 0.8), 2))
                continue
        except NoSuchElementException:
            pass
        # 提示按钮
        tipBtn = browser.find_element_by_class_name('tips')
        print('--> 当前题目进度：' + str(questionIndex) + '/' + str(questionCount))
        tipBtn.click()
        sleep(round(uniform(0.2, 0.8), 2))
        try:
            # 获取所有提示内容
            tipsContent = browser.find_element_by_class_name('line-feed').find_elements_by_tag_name('font')
            sleep(round(uniform(0.2, 0.8), 2))
            tipBtn.click()
            tips = []
            tips.clear()
            for tip in tipsContent:
                tips.append(tip.text)

            if '单选题' in questionType:
                # 选择题，获取所有选项
                options = browser.find_elements_by_class_name('choosable')
                if len(tips) == 0:
                    sleep(round(uniform(0.2, 0.8), 2))
                    options[0].click()
                else:
                    ansDict = {}  # 存放每个选项与提示的相似度
                    for i in range(len(options)):
                        ansDict[i] = SequenceMatcher(None, tips[0], options[i].text[3:]).ratio()
                    ansDict = sorted(ansDict.items(), key=lambda x: x[1], reverse=True)
                    # print(ansDict)
                    print('-->    最大概率选项： ' + options[ansDict[0][0]].text[0])
                    options[ansDict[0][0]].click()

                sleep(round(uniform(0.2, 0.8), 2))
                okBtn.click()

            elif '多选题' in questionType:
                # 选择题，获取所有选项
                options = browser.find_elements_by_class_name('choosable')
                qWord = browser.find_element_by_class_name('q-body').text
                bracketCount = len(findall('（）', qWord))
                if len(options) == bracketCount:
                    select_all(options)
                else:
                    if len(tips) == 0:
                        sleep(round(uniform(0.2, 0.8), 2))
                        options[0].click()
                        sleep(round(uniform(0.2, 0.8), 2))
                        options[1].click()
                    else:
                        # 如果选项数量多于提示数量，则匹配出最可能的选项
                        if len(options) > len(tips):
                            ans = []  # 存放匹配出的最终结果
                            for i in range(len(tips)):
                                ansDict = {}  # 存放每个选项与提示的相似度
                                for j in range(len(options)):
                                    ansDict[j] = SequenceMatcher(None, tips[i], options[j].text[3:]).ratio()
                                # print(ansDict)
                                ansDict = sorted(ansDict.items(), key=lambda x: x[1], reverse=True)
                                ans.append(ansDict[0][0])
                            ans = list(set(ans))
                            # print(ans)
                            print('-->    最大概率选项：', end='')
                            for i in range(len(ans)):
                                print(' ' + options[ans[i]].text[0], end='')
                            print()
                            for i in range(len(ans)):
                                sleep(round(uniform(0.2, 0.8), 2))
                                options[ans[i]].click()
                        # 如果选项数量和提示数量相同或少于提示数量，则全选
                        else:
                            select_all(options)

                sleep(round(uniform(0.2, 0.8), 2))
                okBtn.click()

            elif '填空题' in questionType:
                # 填空题，获取所有输入框
                blanks = browser.find_elements_by_class_name('blank')
                tips_i = 0
                for i in range(len(blanks)):
                    sleep(round(uniform(0.2, 0.8), 2))
                    if len(tips) > tips_i and tips[tips_i].strip() == '':
                        tips_i += 1
                    try:
                        blank_ans = tips[tips_i]
                    except:
                        blank_ans = '未找到提示'
                    print('-->    第{0}空答案可能是： {1}'.format(i + 1, blank_ans))
                    blanks[i].send_keys(blank_ans)
                    tips_i += 1

                sleep(round(uniform(0.2, 0.8), 2))
                okBtn.click()
        except UnexpectedAlertPresentException:
            alert = browser.switch_to.alert
            alert.accept()
            otherPlace = browser.find_element_by_id('app')
            otherPlace.click()
            sleep(round(uniform(0.2, 0.8), 2))
        except WebDriverException:
            print(str(format_exc()))
            print('--> 答题异常，正在重试')
            otherPlace = browser.find_element_by_id('app')
            otherPlace.click()
            sleep(round(uniform(0.2, 0.8), 2))

        if questionIndex == questionCount:
            sleep(round(uniform(0.2, 0.8), 2))
            try:
                submit = browser.find_element_by_class_name('submit-btn')
                submit.click()
                browser.implicitly_wait(10)
                sleep(round(uniform(2.6, 4.6), 2))
            except NoSuchElementException:
                submit = browser.find_element_by_class_name('ant-btn-primary')
                submit.click()
                browser.implicitly_wait(10)
                sleep(round(uniform(2.6, 4.6), 2))
            except UnexpectedAlertPresentException:
                alert = browser.switch_to.alert
                alert.accept()
            print('--> 答题结束')
            break
