目录结构和系统流程
==================

.. note:: 欢迎！当您查看此章节的时候，您已经步入了开发的范畴了！阅读后面的章节有利于您更好的理解桃丽系统的工作原理与。

桃丽系统运行时会调用多个自带的代码文件，确保系统正常运行与工作，下面将阐述其目录结构。

目录结构
--------

.. code-block:: none

	掌控板根目录
	│  boot.py  # 启动文件，内有 BootLoader 模式。
	│  main.py  # 主要代码文件，用于分配显示的页面与处理系统逻辑
	│
	└─TaoLiSystem  # 桃丽系统的代码文件夹
		│  COPYRIGHT  # 版权文件，用于系统关于
		│
		├─core  # 系统核心文件夹
		│      config.py  # 系统配置文件读取工具、全局变量存放位置
		│      sysgui.py  # 系统 GUI 绘制，所有常见 GUI 界面都在这里
		│      utils.py  # 系统零碎的代码集合
		│
		├─data  # 数据存放文件夹
		│      config.ini  # 系统配置文件
		│
		├─modules  # 系统外接的模块文件夹存放位置
		├─page  # 系统的主要页面
		│      home.py  # 主页面
		│      homeFun.py  # 主页面的小功能
		│      plugin.py  # 插件页面
		│      setting.py  # 设置页面
		│      settingFun.py  # 详细设置项
		│
		├─plugins  # 文件文件夹
		│  └─HelloWorld  # 示例插件文件夹
		│         ico.bin  # 插件图标、图片存放文件
		│         __init__.json  # 插件信息文件
		│         __init__.py  # 插件启动代码
		│
		└─static  # 资源文件存放位置
		
系统流程
--------

系统流程主要如下：

* 掌控板启动时，调用 `boot.py` 文件，随后调用主代码文件 `main.py` ，加载系统。
* 加载系统时，会先使用 `gc.collect()` 命令释放多余内存，随后进入启动项判断（是否连接WIFI、是否同步时间等）。
* 最后进入系统的主循环，默认加载页面 `TaoLiSystem/page/home.py` 文件显示主页面。
* 通过 `按键中断 <https://mpython.readthedocs.io/zh/master/tutorials/basics/buttons.html>`_ 来获取用户是否按下 A 键或 B 键，随后切换页面显示。

.. note:: 值得注意的是，默认加载的页面并未写死，是可以修改的。后面将逐步介绍。