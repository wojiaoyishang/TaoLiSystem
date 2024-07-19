:mod:`config` -- 系统配置模块
=============================

:mod:`config` 模块源代码在文件夹 `TaoLiSystem/core/config.py` 下，主要用于配置的写入与读取。

.. module:: config

变量
----

.. py:data:: global_var

	一个字典，用于存放全局变量。

.. py:data:: configData

	:ref:`Config <config-Config>` 类的对象，用于操作系统配置文件。
	
.. py:data:: touchPad_sensitivity
	
	按键灵敏度，加载代码时自动从配置文件中提取。

类
--

.. _config-Config:

.. class:: Config

	操作 ini 配置文件的类，提供了一些基本的操作配置的方法。
	
	.. method:: read(section, key[, default])
	
		* ``section`` -- 配置部分
		* ``key`` -- 配置键
		* ``default`` -- 不存在时，默认返回值，默认为 None 。
		
	.. method:: write(section, key, value)
	
		* ``section`` -- 配置部分
		* ``key`` -- 配置键
		* ``value`` -- 配置值
	
	
	
		
