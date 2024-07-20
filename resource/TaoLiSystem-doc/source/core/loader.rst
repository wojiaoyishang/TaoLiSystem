:mod:`loader` -- 系统初始化模块
===============================

:mod:`loader` 模块源代码在文件夹 `TaoLiSystem/core/loader.py` 下，主要用于系统的初始化。

.. important:: 2024.7.18 新增加的模块，由 `main.py` 调用。

.. module:: loader

变量
----

.. py:data:: pages

	存放系统的界面顺序。

.. py:data:: page_id

	最初加载的页面 ID 。
	
.. py:data:: wait_close
	
	是否准备关闭。
	
.. py:data:: imported_not_modules

	系统一开始导入的模块列表，后续用于切换页面时删除多于加载的模块。

