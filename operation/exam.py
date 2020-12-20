import selenium
from selenium.common.exceptions import WebDriverException
import time
import random
import difflib
import re
from userOperation import check
import os
from selenium import webdriver


def check_exam(browser, examType):
    time.sleep(round(random.uniform(1, 2), 2))
    allExams = browser.find_elements_by_class_name('ant-btn-primary')
    while True:
        flag = True
        for exam in allExams:
            if exam.text == '开始答题' or exam.text == '继续答题':
                browser.execute_script('arguments[0].scrollIntoView();', exam)
                time.sleep(round(random.uniform(1, 2), 2))
                exam.click()
                flag = False
                break
        if flag:
            nextPage = browser.find_element_by_class_name('ant-pagination-next')
            browser.execute_script('arguments[0].scrollIntoView();', nextPage)
            time.sleep(round(random.uniform(1, 2), 2))
            if nextPage.get_attribute('aria-disabled') == 'true':
                if examType == check.CheckResType.WEEKLY_EXAM:
                    print('--> 每周答题：已无可做题目')
                elif examType == check.CheckResType.SPECIAL_EXAM:
                    print('--> 专项答题：已无可做题目')
                return
            nextPage.click()
            time.sleep(round(random.uniform(3, 5), 2))
        else:
            break


def to_exam(browser, examType):
    browser.get('https://www.xuexi.cn/')
    time.sleep(round(random.uniform(1, 2), 2))
    browser.get('https://pc.xuexi.cn/points/my-points.html')
    time.sleep(round(random.uniform(1, 2), 2))

    if examType == check.CheckResType.DAILY_EXAM:
        daily = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[5]/div[2]/div[2]/div')
        browser.execute_script('arguments[0].scrollIntoView();', daily)
        time.sleep(round(random.uniform(1, 2), 2))
        daily.click()
    elif examType == check.CheckResType.WEEKLY_EXAM:
        weekly = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[6]/div[2]/div[2]/div')
        browser.execute_script('arguments[0].scrollIntoView();', weekly)
        time.sleep(round(random.uniform(1, 2), 2))
        weekly.click()
        check_exam(browser, examType)
    elif examType == check.CheckResType.SPECIAL_EXAM:
        special = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[3]/div[2]/div[7]/div[2]/div[2]/div')
        browser.execute_script('arguments[0].scrollIntoView();', special)
        time.sleep(round(random.uniform(1, 2), 2))
        special.click()
        check_exam(browser, examType)

    time.sleep(round(random.uniform(2, 4), 2))
    run_exam(browser)


def run_exam(browser):
    # url = 'https://pc.xuexi.cn/points/exam-practice.html'
    # url = 'https://pc.xuexi.cn/points/exam-paper-detail.html?id=297'
    # browser.get(url)
    while True:
        content = browser.find_element_by_class_name('ant-breadcrumb')
        browser.execute_script('arguments[0].scrollIntoView();', content)
        time.sleep(round(random.uniform(2, 3), 2))
        # 题目类型
        questionType = browser.find_element_by_class_name('q-header').text
        # print(questionType)
        # 当前题目的坐标
        questionIndex = int(browser.find_element_by_class_name('big').text)
        # 题目总数
        questionCount = int(re.findall('/(.*)', browser.find_element_by_class_name('pager').text)[0])
        # 确定按钮
        okBtn = browser.find_element_by_class_name('ant-btn-primary')
        try:
            browser.find_element_by_class_name('answer')
            if okBtn.text == '下一题':
                okBtn.click()
                time.sleep(round(random.uniform(2, 3), 2))
                continue
        except selenium.common.exceptions.NoSuchElementException:
            pass
        # 提示按钮
        tipBtn = browser.find_element_by_class_name('tips')
        print('--> 当前题目进度：' + str(questionIndex) + '/' + str(questionCount))
        tipBtn.click()
        time.sleep(round(random.uniform(0.5, 1.5), 2))
        try:
            # 获取所有提示内容
            tipsContent = browser.find_element_by_class_name('line-feed').find_elements_by_tag_name('font')
            time.sleep(round(random.uniform(0.5, 1.5), 2))
            tipBtn.click()
            tips = []
            tips.clear()
            for tip in tipsContent:
                tips.append(tip.text)
                # print('--> #提示# ' + tip.text)

            if '单选题' in questionType:
                # 选择题，获取所有选项
                options = browser.find_elements_by_class_name('choosable')
                # for text in options:
                #     print('-->    ' + text.text)
                ansDict = {}  # 存放每个选项与提示的相似度
                for i in range(len(options)):
                    ansDict[i] = difflib.SequenceMatcher(None, tips[0], options[i].text[3:]).ratio()
                ansDict = sorted(ansDict.items(), key=lambda x: x[1], reverse=True)
                # print(ansDict)
                print('-->    最大概率选项： ' + options[ansDict[0][0]].text[0])
                options[ansDict[0][0]].click()

                time.sleep(round(random.uniform(0.5, 2), 2))
                okBtn.click()

            elif '多选题' in questionType:
                # 选择题，获取所有选项
                options = browser.find_elements_by_class_name('choosable')
                # for text in options:
                #     print('-->    ' + text.text)
                # 如果选项数量多于提示数量，则匹配出最可能的选项
                if len(options) > len(tips):
                    ans = []  # 存放匹配出的最终结果
                    for i in range(len(tips)):
                        ansDict = {}  # 存放每个选项与提示的相似度
                        for j in range(len(options)):
                            ansDict[j] = difflib.SequenceMatcher(None, tips[i], options[j].text[3:]).ratio()
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
                        time.sleep(round(random.uniform(0.5, 1.5), 2))
                        options[ans[i]].click()
                # 如果选项数量和提示数量相同或少于提示数量，则全选
                else:
                    print('-->    最大概率选项：', end='')
                    for i in range(len(options)):
                        print(' ' + options[i].text[0], end='')
                    print()
                    for i in range(len(options)):
                        time.sleep(round(random.uniform(0.5, 1.5), 2))
                        options[i].click()

                time.sleep(round(random.uniform(0.5, 2), 2))
                okBtn.click()

            elif '填空题' in questionType:
                # 填空题，获取所有输入框
                blanks = browser.find_elements_by_class_name('blank')

                if len(blanks) <= len(tips):
                    for i in range(len(blanks)):
                        time.sleep(round(random.uniform(0.5, 1.5), 2))
                        print('-->    第{0}空答案可能是： {1}'.format(i + 1, tips[i]))
                        blanks[i].send_keys(tips[i])
                else:
                    for i in range(len(blanks)):
                        time.sleep(round(random.uniform(0.5, 1.5), 2))
                        print('-->    未找到提示')
                        blanks[i].send_keys('不知道')

                time.sleep(round(random.uniform(0.5, 2), 2))
                okBtn.click()
            # print()

        except WebDriverException as e:
            print(e)
            print('--> 答题异常，正在重试')
            otherPlace = browser.find_element_by_id('app')
            otherPlace.click()
            time.sleep(round(random.uniform(0.5, 2), 2))

        if questionIndex == questionCount:
            try:
                submit = browser.find_element_by_class_name('submit-btn')
                submit.click()
                time.sleep(round(random.uniform(0.5, 2), 2))
            except selenium.common.exceptions.NoSuchElementException:
                pass
            print('--> 答题结束')
            break

