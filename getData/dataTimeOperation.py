import time
import datetime
import json
import pathlib


def get_diff(date_str):
    """
    获取两个日期之差
    :param date_str: 日期字符串
    :return: 差值
    """
    now_time = time.localtime(time.time())
    compare_time = time.strptime(date_str, "%Y-%m-%d")
    date1 = datetime.datetime(compare_time[0], compare_time[1], compare_time[2])
    date2 = datetime.datetime(now_time[0], now_time[1], now_time[2])
    diff_days = (date2 - date1).days
    return diff_days


def is_get_data(file_type):
    dataPath = './data/lastTime.json'
    if not pathlib.Path(dataPath).is_file():
        with open(dataPath, 'w', encoding='utf-8') as f:
            dataDict = {
                'articles': '2020-01-01',
                'videos': '2020-01-01'
            }
            f.write(json.dumps(dataDict, ensure_ascii=False, indent=4))
        return True
    else:
        with open(dataPath, 'r', encoding='utf-8') as f:
            lastTime = json.loads(f.read())
            diff_days = get_diff(lastTime[file_type])
    return diff_days > 30


def set_time(file_type):
    dataPath = './data/lastTime.json'
    with open(dataPath, 'r', encoding='utf-8') as f:
        dataDict = json.loads(f.read())
        dataDict[file_type] = time.strftime("%Y-%m-%d", time.localtime())
    with open(dataPath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dataDict, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    print(get_diff('2020-12-1'))
    is_get_data('articles')
