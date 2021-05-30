# -*- encoding: utf-8 -*-
from requests import get
from re import compile
from subprocess import Popen, PIPE, call
from traceback import format_exc
from zipfile import ZipFile


def do(program_path):
    try:
        url = 'http://npm.taobao.org/mirrors/chromedriver/'
        latest_version = get_latest_version(url)
        version = get_version(program_path)
        if version != latest_version:
            print('--> 当前chromedriver不是最新，准备进行更新')
            download_url = url + latest_version + '/chromedriver_win32.zip'  # 拼接下载链接
            download_chromedriver(download_url)
            unzip_file(program_path)
            print('--> chromedriver更新成功\n')
        return True
    except:
        print(str(format_exc()))
        print('--> 程序异常，请确保你的chrome浏览器是最新版本，然后重启脚本')
        call('pause', shell=True)
        return False


def get_latest_version(url):
    """
    查询最新chromedriver版本号
    :param url: chromedriver链接
    :return: 版本号
    """
    rep = get(url).text
    time_list = []  # 用来存放版本时间
    time_version_dict = {}  # 用来存放版本与时间对应关系
    result = compile(r'\d.*?/</a>.*?Z').findall(rep)  # 匹配文件夹（版本号）和时间
    for i in result:
        time = i[-24:-1]  # 提取时间
        version = compile(r'.*?/').findall(i)[0]  # 提取版本号
        time_version_dict[time] = version  # 构建时间和版本号的对应关系，形成字典
        time_list.append(time)  # 形成时间列表
    latest_version = time_version_dict[max(time_list)][:-1]  # 用最大（新）时间去字典中获取最新的版本号
    return latest_version


def download_chromedriver(download_url):
    """
    下载chromedriver
    :param download_url: 下载链接
    """
    file = get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:  # 保存文件到脚本所在目录
        zip_file.write(file.content)
        print('--> chromedriver下载成功')


def get_version(path):
    """
    获取当前chromedriver版本号
    :return:
    """
    import os
    version_info = Popen([os.path.join(path, 'chromedriver.exe'), '--version'], shell=True,
                         stdout=PIPE).stdout.read().decode()
    return version_info.split(' ')[1]


def unzip_file(path):
    """
    解压chromedriver.zip到指定目录
    :param path: 解压目录
    """
    f = ZipFile('chromedriver.zip', 'r')
    for file in f.namelist():
        f.extract(file, path)
    f.close()
    print('--> 解压成功')
    import os
    os.remove('chromedriver.zip')
    print('--> 压缩包已删除')
