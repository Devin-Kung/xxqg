# -*- encoding: utf-8 -*-
import os

from requests import get
from re import compile,match
from subprocess import check_output, call
from traceback import format_exc
from zipfile import ZipFile
# import winreg
from json import loads
import platform
from os import path
from chromedriver_autoinstaller.utils import get_chrome_version,get_platform_architecture
(PLATFROME, ARCH) = get_platform_architecture()
CHROMEDIRVER="chromedriver.exe" if PLATFROME == 'win' else 'chromedriver'


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
        url = 'https://npm.taobao.org/mirrors/chromedriver/'
        chrome_version = '.'.join(get_chrome_version().split('.')[: 3])  # 当前Chrome版本号(前三位)
        version = '.'.join(get_version(path.join(program_path, CHROMEDIRVER)).split('.')[: 3])     # 当前ChromeDriver版本号(前三位)
        if not chrome_version == version:
            print('--> 当前ChromeDriver版本号和Chrome浏览器版本号不一致，准备进行更新')
            latest_version = get_download_version(chrome_version, url)
            if PLATFROME == 'mac':
                    download_url = url + latest_version + '/chromedriver_mac64.zip'  # 拼接下载链接
            else:
                download_url = url + latest_version + '/chromedriver_win32.zip'  # 拼接下载链接
            download_chromedriver(download_url)
            unzip_file(program_path)
            if PLATFROME == 'mac':
                os.chmod(CHROMEDIRVER, 766)
            print('--> ChromeDriver更新成功\n')
        return True
    except:
        print(str(format_exc()))
        print('--> 程序异常，请确保你的chrome浏览器是最新版本，然后重启脚本')
        call('pause', shell=True)
        return False


def get_download_version(current_version, url):
    """
    根据本地Chrome版本号获取可下载的ChromeDriver版本号
    :param current_version: 当前本地Chrome版本号前三位
    :param url: ChromeDriver链接
    :return: 完整版本号
    """
    rep = get(url).text
    version_list = []  # 存放版本号
    result = compile(r'\d.*?/</a>.*?Z').findall(rep)  # 匹配文件夹（版本号）和时间
    for i in result:
        version = compile(r'.*?/').findall(i)[0][:-1]  # 提取版本号
        version_list.append(version)
    version_list.reverse()
    download_version = version_list[0]
    for v in version_list:
        if compile(r'^[1-9]\d*\.\d*.\d*').findall(v)[0] == current_version:
            download_version = v
            break
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
    try:
        version = check_output([path, '-v'])
        version = match(r'.*?([\d.]+).*?', version.decode('utf-8'))[1]
        return version
    except Exception:
        return '0.0.0'


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

