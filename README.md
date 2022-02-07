# 陶丽掌控板系统

#### 故事以及介绍
信息技术必修二的某一章中有关于开发板micro:bit的介绍，这吸引了我的注意。便促使了我从信息老师陶丽那里“借”了一本信息技术必修二的教师用书，并开始了一系列的探索。

从教师用书里面发现了一个叫做掌控板的开发板。于是在高一的寒假我打算制作一个“掌控板系统”来送给我们貌美如花、聪明、美丽、睿智、优雅、智商堪比爱因斯坦（此处省略一万字彩虹屁）、像 **桃（陶）** 花一样美 **丽** 的信息老师陶丽。在征得了她的同意后，我决定将她的名字引用为系统的名字——“陶丽系统 TaoLiSystem”（简称 “TLCS”）。

经过不懈的努力与开发，陶丽系统的雏形逐渐完善。

下面我将介绍陶丽系统的各个框架。

#### 软件架构

```
TaoLiSystem
│  boot.py                  # 掌控板启动一定会运行的文件，非必要，这里面设计了开机动画
│  main.py                  # 陶丽系统主要引导文件，从这里开始会调用 TaoLiSystem 文件夹内的文件
│  tips.py                  # 没什么用的文件，用于开发者开发时记录的“记事本”
└─TaoLiSystem               # 陶丽系统的核心文件会放在 TaoLiSystem 中
    │  config.json          # 陶丽系统的配置文件
    │  config.py            # 陶丽系统调用配置文件的模块
    │  function.py          # 陶丽系统整合的使用函数的模块
    │  image.py             # 陶丽系统存储小图片的模块
    │  ItemSelector.py      # 陶丽系统的物品选择器模块
    │  loader.py            # 陶丽系统的初始化加载
    │  morseType.py         # 陶丽系统的摩尔斯电码输入模块
    │  TXTreader.py         # 陶丽系统的文本阅读模块
    │  wifi.py              # 陶丽系统用于控制wifi的模块
    ├─font                  # 陶丽系统的调用的字体所放的目录
    │      arlrdbd.py       # Arial Rounded MT Bold 字体 (个人使用，不得商用)
    │      HYShiGuangTiJ.py # 汉仪时光体简 Regular 字体 (个人使用，不得商用)
    ├─page                  # 陶丽系统页面存放目录
    │      home.py          # 陶丽系统主页源码
    │      plugin.py        # 陶丽系统插件页源码
    │      setting.py       # 陶丽系统设置页源码
    ├─picture               # 陶丽系统图片放置目录
    │      loadingPage.bmp  # 加载页面图片
    │      waitingPage.bmp  # 等待页面图片
    └─plugin                # 插件存放目录
```



#### 安装教程

1.  xxxx
2.  xxxx
3.  xxxx

#### 使用说明

1.  xxxx
2.  xxxx
3.  xxxx

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
