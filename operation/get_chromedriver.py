# -*- encoding: utf-8 -*-
import re
from requests import get
from re import compile
from subprocess import Popen, PIPE, call
from traceback import format_exc
from zipfile import ZipFile
import winreg
from json import loads


def do(program_path):
    """
    检测并更新ChromeDriver
    :param program_path: ChromeDriver路径（文件夹路径）
    :return: 执行结果 True：执行成功，False：执行失败
    """
    settings_path = 'data/settings.json'
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = f.read()
    settings = loads(settings)
    if settings['自动更新ChromeDriver'] != "true":
        return True
    try:
        url = 'https://registry.npmmirror.com/-/binary/chromedriver/'
        chrome_version = get_chrome_version()  # 当前Chrome版本号(前三位)
        version = get_version(program_path)  # 当前ChromeDriver版本号(前三位)
        if chrome_version != version:
            print('--> 当前ChromeDriver版本号和Chrome浏览器版本号不一致，准备进行更新')
            latest_version = get_download_version(chrome_version)
            download_url = url + latest_version + '/chromedriver_win32.zip'  # 拼接下载链接
            download_chromedriver(download_url)
            unzip_file(program_path)
            print('--> ChromeDriver更新成功\n')
        return True
    except:
        print(str(format_exc()))
        print('--> 程序异常，请确保你的chrome浏览器是最新版本，然后重启脚本')
        call('pause', shell=True)
        return False


def get_download_version(current_version):
    """
    根据本地Chrome版本号获取可下载的ChromeDriver版本号
    :param current_version: 当前本地Chrome版本号前三位
    :return: 完整版本号
    """
    google_api_url = 'https://registry.npmmirror.com/-/binary/chromedriver/'
    rep = loads(get(google_api_url).content.decode('utf-8'))
    version_list = []

    for item in rep:
        letter_re = re.compile(r'[A-Za-z]', re.S)
        letter_res = re.findall(letter_re, item['name'])
        if len(letter_res):
            continue
        version_list.append(item)

    download_version = version_list[len(version_list) - 1]
    for item in version_list:
        if compile(r'^[1-9]\d*\.\d*.\d*').findall(item['name'])[0] == current_version:
            download_version = item['name'][:-1]
    return download_version


def download_chromedriver(download_url):
    """
    下载chromedriver
    :param download_url: 下载链接
    """
    file = get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:  # 保存文件到脚本所在目录
        zip_file.write(file.content)
        print('--> ChromeDriver下载成功')


def get_version(path):
    """
    获取当前ChromeDriver版本号前三位
    :param path: chromedriver文件夹路径
    :return: 版本号前三位
    """
    import os
    version_info = Popen([os.path.join(path, 'chromedriver.exe'), '--version'], shell=True,
                         stdout=PIPE).stdout.read().decode()
    return compile(r'^[1-9]\d*\.\d*.\d*').findall(version_info.split(' ')[1])[0]


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


def get_chrome_version():
    """
    获取当前Chrome浏览器版本号
    :return: 版本号前三位
    """
    version_re = compile(r'^[1-9]\d*\.\d*.\d*')
    try:
        # 从注册表中获得版本号
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
        version, _ = winreg.QueryValueEx(key, 'version')
        return version_re.findall(version)[0]  # 返回前3位版本号
    except WindowsError as e:
        print('Chrome版本检查失败:{}'.format(e))
