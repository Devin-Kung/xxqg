# 此脚本最后测试于2021/2/2，运行正常

# 声明

1. 本项目仅用于学习python，严禁将其用于任何商业用途
2. 请端正学习态度，严禁将本项目用于任何形式的刷分行为

# 开始：

0. 可以将源码下载或clone到本地仓库，自行编译运行，也可以在[ Release ](https://github.com/PRaichu/xxqg/releases)中下载我已经编译了的版本
1. 请确保你电脑中已经安装最新chrome浏览器，没有安装请先去  https://www.google.cn/chrome/  下载安装
2. 点击运行 `xuexi.exe` ，根据提示进行操作
3. 脚本运行过程中请勿关闭或最小化浏览器，否则可能会失败，并且可能有检测风险
4. 可将脚本控制台置于最前，查看运行进度
5. 【注意】压缩包中已内置`chromedriver.exe`，但其版本为`88.0.4324.96`，如果你的Chrome浏览器版本高于此版本，请去 http://npm.taobao.org/mirrors/chromedriver/ 下载你浏览器的对应版本（版本号与浏览器版本号前三位一致即可），解压后替换原版本

# 安全：

1. 为了确保账号的安全，建议刷了几天脚本后人工刷一两天
2. 请勿频繁刷题，高频刷题可能有风险，“每周答题”、“专项答题”一周的频率不超过3次为好

# 设置：

1. 支持对自动答题、浏览文章、观看视频进行设置
2. 设置可以在 `data/settings.json`中修改，true表示执行，false表示不执行 
3. 【注意】只有当“自动答题”为true时，其他答题设置才会生效

# 已知问题：

1. 如果win10报毒，加白名单就好，开源项目放心使用
2. 如果脚本控制台长时间不动，可以尝试输入回车或重启脚本，暂时不知道原因
3. 答题时如果报如下错：<br>
   `Message: element click intercepted: Element xxxxxxxxxxx is not clickable at point (xxx, xxx). Other element would receive the click: xxxxxxxxxxxxxxxxxxxx`<br>这是因为浏览器窗口太小了，尝试将浏览器全屏或将窗口拉大一点
4. 如果使用时还有其他问题，欢迎发`issue`反馈

# 运行效果图


<img src="https://github.com/PRaichu/xxqg/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE1.png?raw=true" alt="观看视频/文章效果图" style="zoom:50%;" />

<img src="https://github.com/PRaichu/xxqg/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE2.png?raw=true" alt="答题效果图" style="zoom:50%;" />

<img src="https://github.com/PRaichu/xxqg/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE3.png?raw=true" alt="结束效果图" style="zoom: 80%;" />

# 项目结构树

```text
│  xuexi.py
│  xxqg.ico
│  __init__.py
│
├─data
│      articles.json
│      lastTime.json
│      settings.json
│      videos.json
│
├─getData
│      dataTimeOperation.py
│      get_article.py
│      get_video.py
│      __init__.py
│
├─operation
│      exam.py
│      scan_article.py
│      watch_video.py
│      __init__.py
│
└─userOperation
        check.py
        login.py
        logout.py
        __init__.py
```