# -*- encoding: utf-8 -*-
from traceback import format_exc
from requests import get
from json import loads
from getData.version import VERSION


def get_latest_version():
    url = 'https://api.github.com/repos/PRaichu/xxqg/releases/latest'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }
    try:
        response_data = get(url=url, headers=headers).content
        latest_version = loads(response_data)['tag_name']
        return latest_version
    except ValueError:
        print(str(format_exc()))
        print('--> \033[31m请求版本号失败，请检查是否开启了VPN或代理软件，如果开启了请关闭后再试\033[0m')
        print('--> \033[31m此处报错为版本号请求失败，不会影响程序运行，无需关闭程序\033[0m')
        return None
    except:
        print(str(format_exc()))
        print('--> \033[31m请求版本号失败，请检查你的网络环境\033[0m')
        print('--> \033[31m此处报错为版本号请求失败，不会影响程序运行，无需关闭程序\033[0m')
        return None


def check():
    latest_version = get_latest_version()
    if latest_version is not None and VERSION != latest_version:
        print('--> 程序当前版本号：{}，最新版本号：\033[32m{}\033[0m，该版本可能已过时，建议下载最新版本以获得更好的体验！'.format(VERSION, latest_version))
        print('--> 下载地址：https://github.com/PRaichu/xxqg/releases/latest')
        print('--> 当然，你也可以选择不更新，这不会影响当前程序的使用！\n')


if __name__ == '__main__':
    check()
