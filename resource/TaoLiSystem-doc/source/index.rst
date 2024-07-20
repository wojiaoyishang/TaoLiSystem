目录索引
==================

.. note:: 你好鸭！欢迎查看桃丽系统帮助文档，您可以查看 :ref:`welcome` 章节来获得更多信息。 系统目前处于公测阶段，可能存在诸多问题，如果遇到了系统的 BUG 请尽量找出 BUG 的复现方法 方便定位问题，有问题、建议、创意请提 Issues，有能力的同学可以提交 PR。

.. important:: 2024年7月优化了掌控板代码，修正了部分 BUG ，感谢 `我叫罗米奇 <https://gitee.com/romich>`_ 提供的修正。 另外，增加了新的构建工具，可以自动下载代码到掌控板，不需要下载额外的工具，但是您的计算机必须装有 Python 或者其他可以运行 Python 代码的工具。 关于桃丽系统文档，由于 Gitee Page 的服务调整，帮助文档已迁移到我自己的服务器上。

.. warning:: 2023年8月更新了桃丽系统 v2.0.0 版本，进行了全面重置，原版本查看分支 v1.0.0 ，v1.0.0 版本已不再更新和维护。

更新日志
--------

2024.7.19
~~~~~~~~~

+ **Chore:** 增加了构建工具和刷入工具，可以一键构建与刷入系统便于使用。制作了掌控板系统配置程序，方便调试修改配置。
+ **Chore:** 调整了目录架构，增加了 ``resource`` 文件夹存放开发时使用的工具、资源。
+ **Chore:** 移除了不常用的插件，放在了 ``resource/plugins`` 文件夹下。
+ **Enhancement:** 优化了系统起始入口的代码，引入 loader 进行加载系统，面向对象，便于开发。相关文件： ``main.py``  ``TaoLiSystem/core/loader.py``
+ **Enhancement:** 优化了设置页面的代码，使代码变得更易于查看。 ``TaoLiSystem/page/settingFun.py``
+ **Feature:** 允许在掌控板中切换首页（切换表盘），并同时提供了 default（默认） 和 easy（示例首页） 两种首页样式，其他首页仍在开发欢迎提交 PR。相关文件： ``TaoLiSystem/page/home.py`` -> ``TaoLiSystem/page/home/``
+ **Feature:** 允许首页（表盘）自定义个性化设置和编排页面，并且支持热更新，相关内容请查看文档。 相关文件： ``TaoLiSystem/page/home/``
+ **Feature:** 修改设置项，将 ``熄屏设置`` 更改为 ``屏幕设置``。 相关文件： ``TaoLiSystem/page/settingFun.py``
+ **Feature:** 新增浅度睡眠、深度睡眠、软重启、硬重启等设置项。 相关文件： ``TaoLiSystem/page/settingFun.py``
+ **Feature:** 新增熄屏时自动进入浅度睡眠状态选项，**调整原本熄屏唤醒用 A/B 键唤醒为只能用 A 键唤醒。** 相关文件： ``TaoLiSystem/page/settingFun.py``
+ **Feature:** 更新蓝牙设置功能和蓝牙信息查看（尚未测试），感谢 `我叫罗米奇 <https://gitee.com/romich>`_。 相关文件： ``TaoLiSystem/page/settingFun.py``  ``TaoLiSystem/core/utils.py``
+ **Fix:** 修复了首页熄屏无法唤醒问题，修复熄屏设置无效的问题。 相关文件： ``TaoLiSystem/page/settingFun.py``
+ **Fix:** 修复了时间手动设置失效的问题和无法手动同步时间的问题。 `#I9KT1M <https://gitee.com/wojiaoyishang/TaoLiSystem/issues/I9KT1M>`_ 相关文件： ``TaoLiSystem/page/settingFun.py``
+ **Fix:** 修复了在文字输入页面按下 O 键无效的问题，感谢 `我叫罗米奇 <https://gitee.com/romich>`_ 的修正，并在文字输入页面增加了几个可以输入的字符。 相关文件： ``TaoLiSystem/core/sysgui.py``
+ **Fix:** 修复了在切换页面时反复按下按钮，无法切换的问题。 相关文件： ``TaoLiSystem/core/loader.py``
+ **Refactor:** 重构了配置文件的读取与设置，使用内置的 btree 数据库进行存储设置，速度加快。相关文件： ``TaoLiSystem/core/config.py``


.. toctree::
    :maxdepth: 1
    :caption: 介绍、配置与使用

    welcome/index

.. toctree::
    :maxdepth: 1
    :caption: 项目开发说明
	
    develop/index
	
.. toctree::
    :maxdepth: 1
    :caption: 核心模块说明
	
    core/index
	
.. toctree::
    :maxdepth: 1
    :caption: 插件开发说明
	
    plugin/index
	