<p align="center">
  <img width="200" src="https://github.com/PRaichu/xxqg/blob/master/xuexi.jpg?raw=true" alt="xuexi">
</p>

<p align="center">
   <img src="https://img.shields.io/badge/python-3.6+-green" alt="python">
   <img src="https://img.shields.io/badge/chrome-87.0.4280+-yellow" alt="chrome">
   <a href="https://github.com/PRaichu/xxqg/releases/latest">
      <img src="https://img.shields.io/github/v/release/praichu/xxqg" alt="release">
   </a>
   <a href="https://github.com/PRaichu/xxqg/blob/master/LICENSE">
      <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
   </a>
   <img src="https://img.shields.io/github/stars/PRaichu/xxqg.svg" alt="stars">
   <img src="https://img.shields.io/github/forks/PRaichu/xxqg.svg" alt="forks">
   <img src="https://img.shields.io/github/downloads/PRaichu/xxqg/total" alt="downloads">
</p>

# 此脚本最后测试于2022/03/08，运行正常

# 声明

0. 使用此脚本则默认同意以下声明
1. 本项目仅用于学习Python，严禁将其用于任何违法用途
2. 请端正学习态度，严禁将本项目用于任何形式的刷分行为
3. 因使用此脚本造成的账号风控、账号封禁等后果，均自行承担

# 特色

1. 支持浏览文章，观看视频，自动答题（每日答题，每周答题，专项答题），一天45分
2. 无需手动操作，浏览器全程静音，无感刷视频
3. 全程无人值守，结束任务后自动关闭浏览器
4. 多种随机操作，模拟真人操作，提高安全性
5. 软件包兼容win10/11（其他系统可clone项目运行`xuexi.py`）

# 开始：

0. 可以将源码下载或clone到本地仓库，自行编译运行，也可以在[ Release ](https://github.com/PRaichu/xxqg/releases) 中下载我已经编译了的版本
1. 请确保你电脑中已经安装最新chrome浏览器，没有安装请先去  https://www.google.cn/chrome/ 下载安装
2. 点击运行 `xuexi.exe` ，根据提示进行操作
3. 脚本运行过程中请勿关闭或最小化浏览器，否则可能会失败，并且可能有检测风险
4. 可将脚本控制台置于最前，查看运行进度

# 安全：

1. 为了确保账号的安全，建议刷了几天脚本后人工刷一两天
2. 请勿频繁刷题，高频刷题可能有风险

# 设置：

1. 支持对自动答题、浏览文章、观看视频、更新驱动等进行设置
2. 设置可以在 `data/settings.json`中修改，true表示执行，false表示不执行 
3. 【注意】只有当“自动答题”为true时，其他答题设置才会生效

# 已知问题：

1. 如果win10/11报毒，加白名单就好，这是Python打包的问题，与程序无关，开源项目放心使用，不放心可以clone源码运行
2. 如果脚本控制台长时间不动，可以尝试输入回车或重启脚本
3. 如果使用时还有其他问题，欢迎提`issue`反馈

# 打包

如果有小伙伴需要自己修改代码打包项目的，可以使用`pyinstaller`

1. 安装 

```pip install pyinstaller```

2. 在终端进入项目文件夹，执行如下命令，参数可以根据自己需要修改 

```pyinstaller -F -c -i .\xxqg.ico -p 项目路径 .\xuexi.py``` 

# 运行效果图

<img src="https://github.com/PRaichu/xxqg/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE1.png?raw=true" alt="程序效果图" style="zoom:50%;" />

<img src="https://github.com/PRaichu/xxqg/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE2.png?raw=true" alt="观看视频效果图" style="zoom:50%;" />

<img src="https://github.com/PRaichu/xxqg/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE3.png?raw=true" alt="浏览文章效果图" style="zoom: 80%;" />

<img src="https://github.com/PRaichu/xxqg/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE4.png?raw=true" alt="答题效果图" style="zoom: 80%;" />

# 项目结构树

```text
+--custom                            # 自定义webdriver模块
|      +--xuexi_chrome.py
|      +--__init__.py
+--data                              # 程序运行所需数据文件及配置文件
|      +--articles.json
|      +--lastTime.json
|      +--settings.json
|      +--videos.json
+--getData                           # 数据获取模块
|      +--dataTimeOperation.py
|      +--get_article.py
|      +--get_video.py
|      +--version.py
|      +--__init__.py
+--operation                         # 程序核心模块
|      +--check_version.py
|      +--exam.py
|      +--get_chromedriver.py
|      +--scan_article.py
|      +--watch_video.py
|      +--__init__.py
+--userOperation                     # 用户相关模块
|      +--check.py
|      +--login.py
|      +--logout.py
|      +--__init__.py
+--xuexi.py                          # 主程序入口
+--__init__.py
```

## License

[MIT](https://github.com/PRaichu/xxqg/blob/master/LICENSE)

Copyright (c) 2020-present PRaichu