# -*- encoding: utf-8 -*-
from time import localtime, strptime, strftime, time
from datetime import datetime
from json import loads, dumps
from pathlib import Path


def get_diff(date_str):
    """
    获取两个日期之差
    :param date_str: 日期字符串
    :return: 差值
    """
    now_time = localtime(time())
    compare_time = strptime(date_str, "%Y-%m-%d")
    date1 = datetime(compare_time[0], compare_time[1], compare_time[2])
    date2 = datetime(now_time[0], now_time[1], now_time[2])
    diff_days = (date2 - date1).days
    return diff_days


def is_get_data(file_type):
    data_path = './data/lastTime.json'
    if not Path(data_path).is_file():
        with open(data_path, 'w', encoding='utf-8') as f:
            data_dict = {
                'articles': '2020-01-01',
                'videos': '2020-01-01'
            }
            f.write(dumps(data_dict, ensure_ascii=False, indent=4))
        return True
    else:
        with open(data_path, 'r', encoding='utf-8') as f:
            last_time = loads(f.read())
            diff_days = get_diff(last_time[file_type])
    return diff_days > 30


def set_time(file_type):
    data_path = './data/lastTime.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        data_dict = loads(f.read())
        data_dict[file_type] = strftime("%Y-%m-%d", localtime())
    with open(data_path, 'w', encoding='utf-8') as f:
        f.write(dumps(data_dict, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    print(get_diff('2020-12-1'))
    is_get_data('articles')
