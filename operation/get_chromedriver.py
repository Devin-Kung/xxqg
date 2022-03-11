# -*- encoding: utf-8 -*-
# FROM: https://github.com/PRaichu/xxqg/blob/master/operation/get_chromedriver.py
from requests import get
from urllib.parse import urljoin
from re import compile
from subprocess import Popen, PIPE, call
from traceback import format_exc
from zipfile import ZipFile
import winreg
from json import loads
from pathlib import Path


def do(program_path: Path) -> bool:
    """
    检测并更新ChromeDriver
    :param program_path: ChromeDriver路径（文件夹路径）
    :return: 执行结果 True：执行成功，False：执行失败
    """
    settings_path = Path(__file__).parent.parent / 'data' / 'settings.json'
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings_string = f.read()
    settings = loads(settings_string)
    if settings['自动更新ChromeDriver'] != "true":
        return True
    try:
        url = 'https://registry.npmmirror.com/-/binary/chromedriver/'
        current_chrome_browser_version = get_chrome_browser_version()  # 当前Chrome版本号(前三位)
        version = get_local_chromedriver_version(program_path)  # 当前ChromeDriver版本号(前三位)
        print(f'当前ChromeDriver\t版本号:\t {version}\n'
              f'当前Chrome浏览器\t版本号:\t {current_chrome_browser_version}')
        if current_chrome_browser_version != version:
            print('--> 当前ChromeDriver版本号和Chrome浏览器版本号不一致，准备进行更新')
            remote_latest_version = get_remote_download_version(current_chrome_browser_version)
            download_url = urljoin(url, f'{remote_latest_version}/chromedriver_win32.zip')
            download_chromedriver(download_url, program_path)
            unzip_file(program_path)
            print('--> ChromeDriver更新成功\n')
        else:
            print('--> 当前ChromeDriver版本号和Chrome浏览器版本号一致，无需更新')
        return True
    except Exception:
        print(str(format_exc()))
        print('--> 程序异常，请确保你的chrome浏览器是最新版本，然后重启脚本')
        call('pause', shell=True)
        return False


def get_remote_download_version(current_chrome_browser_version: str) -> str:
    """
    根据本地Chrome版本号获取可下载的ChromeDriver版本号
    :param current_chrome_browser_version: 当前本地Chrome版本号前三位
    :return: 完整版本号
    """
    google_api_url = 'https://registry.npmmirror.com/-/binary/chromedriver/'
    rep = loads(get(google_api_url).content.decode('utf-8'))
    # 去掉其他杂项
    version_list = [item for item in rep
                    if item['date'] == '-' and len(item['name']) > 7
                    ]
    download_version: str = version_list[-1]
    for item in version_list:
        if current_chrome_browser_version in item['name']:
            download_version = item['name'][:-1]
    return download_version


def download_chromedriver(download_url: str, path: Path):
    """
    下载chromedriver
    :param download_url: 下载链接
    """
    file = get(download_url)
    zipfile_path = path / 'chromedriver.zip'
    with open(zipfile_path, 'wb') as zip_file:  # 保存文件到脚本所在目录
        zip_file.write(file.content)
        print('--> ChromeDriver下载成功')


def get_local_chromedriver_version(path: Path) -> str:
    """
    获取当前ChromeDriver版本号前三位
    :param path: chromedriver文件夹路径
    :return: 版本号前三位
    """
    chromedriver_exe_path = path / 'chromedriver.exe'
    print(f'当前chromedriver.exe文件所在目录{chromedriver_exe_path}')
    if not chromedriver_exe_path.exists():
        print('没有chromedriver.exe,需要下载')
        return '0'
    try:
        stdout = Popen([chromedriver_exe_path, '--version'], shell=True,
                             stdout=PIPE).stdout
        if not stdout:
            return '0'
        version_info = stdout.read().decode()
        return compile(r'^[1-9]\d*\.\d*.\d*').findall(version_info.split(' ')[1])[0]
    except Exception as e:
        print(f'--> 执行{chromedriver_exe_path}版本检查错误，直接返回版本号为0')
        print(f'--> {e}')
        return '0'


def unzip_file(path: Path):
    """
    解压chromedriver.zip到指定目录
    :param path: 解压目录
    """
    fp = path / 'chromedriver.zip'
    f = ZipFile(fp, 'r')
    for file in f.namelist():
        f.extract(file, path)
    f.close()
    print('--> 解压成功')
    fp.unlink()
    print('--> 压缩包已删除')


def get_chrome_browser_version() -> str:
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
        print(f'Chrome版本检查失败:\t{e}')
        return '00.00'


if __name__ == '__main__':
    curr_dir = Path(__file__)
    program_path = curr_dir.parent.parent
    do(program_path)
