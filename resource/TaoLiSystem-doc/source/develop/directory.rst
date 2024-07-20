目录结构和系统流程
==================

.. note:: 欢迎！当您查看此章节的时候，您已经步入了开发的范畴了！阅读后面的章节有利于您更好的理解桃丽系统的工作原理。

.. warning:: 由于系统自 v2.1.0 之后，目录结果有所调整，将原有的 `home.py` 修改并移动到了 `TaoLiSystem/page/home/default/__init__.py` 。并将 `homeFun.py` 同时进行相对应的更改。 `main.py` 也有更改，将引入 `loader.py` 将系统编程面向对象。

桃丽系统运行时会调用多个自带的代码文件，确保系统正常运行与工作，下面将阐述其目录结构。

目录结构
--------

项目架构
~~~~~~~~~~

.. code-block:: none
	
	仓库根目录
	│
	├─TaoLiSystem
	│
	└─resource  # 开发资源
		│      @run_build.bat   #  一键写入脚本
		│      @run_setting.bat  #  一键设置脚本
		│      build.py  #  写入脚本源代码
		│      setting.py  #  设置脚本源代码
		│      setting_instructions.py  #  设置脚本源代码中的设置项简介
		│      mpy-cross-vN.exe  #  编译程序
		│      pyboard.py  # 脚本要使用的 pyboard 支持库
		│      pyboard_utils.py  # 拓展的 pyboard 支持库
		│      requirements_check.py  # 脚本进行依赖检查的模块
		│
		├─IMAGES  # 仓库的图片存放文件夹
		├─plugins  # 可选用的插件，需要请拷到 TaoLiSystem 的 plugins 文件夹下
		├─TaoLiSystem-doc  # 开发文档源文件
		└─binpython  # binpython 开源项目编译的文件，用于无 Python 运行脚本
			

系统架构
~~~~~~~~~~

.. code-block:: none

	掌控板根目录
	│  boot.py  # 启动文件，内有 BootLoader 模式。
	│  main.py  # 入口文件，将会调用 loader.py 进行加载。
	│
	└─TaoLiSystem  # 桃丽系统的代码文件夹
		│  COPYRIGHT  # 版权文件，用于系统关于
		│
		├─core  # 系统核心文件夹
		│      config.py  # 系统配置文件读取工具、全局变量存放位置
		│      sysgui.py  # 系统 GUI 绘制，所有常见 GUI 界面都在这里
		│      utils.py  # 系统零碎的代码集合
		│      loader.py  # 用于分配显示的页面与处理系统逻辑
		│
		├─data  # 数据存放文件夹
		│      config.ini  # 系统配置文件
		│
		├─modules  # 系统外接的模块文件夹存放位置
		├─page  # 系统的主要页面
		│  └─home  # 主页面
		│      ├─default
		│      │    __init__.py  # 默认主页，原来的 home.py
		│      │    function.py  # 原来的 homeFun.py
		│      │
		│      └─easy
		│           __init__.py  # 简单示例页面
		│
		│  plugin.py  # 插件页面
		│  setting.py  # 设置页面
		│  settingFun.py  # 详细设置项
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

* 掌控板启动时，调用 `boot.py` 文件，随后调用主代码文件 `main.py` 。
* `main.py` 将会调用 `TaoLiSystem/core/loader.py` 进行加载系统，对于 `loader.py` 的逻辑请查看 main.py 的代码。
* 加载系统时，会先使用 `gc.collect()` 命令释放多余内存，随后进入启动项判断（是否连接WIFI、是否同步时间等）。
* 最后进入系统的主循环，默认加载页面 `TaoLiSystem/page/home.py` 文件显示主页面。
* 通过 `按键中断 <https://mpython.readthedocs.io/zh-cn/master/tutorials/basics/buttons.html>`_ 来获取用户是否按下 A 键或 B 键，随后切换页面显示。

.. note:: 值得注意的是，默认加载的页面并未写死，是可以修改的。后面将逐步介绍。

`main.py` 的代码如下：

.. note:: main_loop() 函数为系统界面绘制正式开始。

.. code-block:: python

	# 系统入口

	# =======================调试命令=======================
	from mpython import *
	if button_a.value() == 0:  # 按下 A 键就退出。防止卡电脑调试。
		raise BaseException("Stop by user.")

	# =======================传递参数=======================
	from TaoLiSystem.core import utils
	def importModule(name):  # 导入模块函数，只有在 main.py 中才能让 exec 不出问题
		_ = []
		exec("import " + name + " as pikachu;_.append(pikachu)", {"_": _})
		return _[0]

	utils.importModule = importModule

	# =======================系统初始化=======================
	from TaoLiSystem.core import loader
	loader.before_init()  # 初始化之前执行
	loader.init() 
	loader.after_init()  # 初始化之后执行
	loader.clean()  # 删去初始化的所有内容
	loader.main_loop()  # 进入系统主循环
    
    



