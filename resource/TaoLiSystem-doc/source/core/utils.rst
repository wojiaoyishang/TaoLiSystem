:mod:`utils` -- 常见功能模块
============================

:mod:`utils` 模块源代码在文件夹 `TaoLiSystem/core/utils.py` 下，汇集了系统反复调用的一些函数，便于系统开发。

.. important:: 2024.7.18 更新深度睡眠 `deepsleep_irc` 与浅度睡眠函数 `lightsleep_irc` 。

.. module:: utils

函数
----

.. function:: importModule(name)

	动态导入一个模块，``importModule`` 函数并不是在 :mod:`utils` 中定义的，`main.py` 调用时会动态创建这个函数。

	* ``name`` -- 导入的模块名称。

.. function:: convert_ms_to_hms(milliseconds)

	转化毫秒到时分秒，返回一个元组 (hours, minutes, seconds, remaining_ms) ，元组内元素均为 `int` 型。

	* ``milliseconds`` -- 毫秒

	例如::

		>>> import time
		>>> from TaoLiSystem.core import utils
		>>> utils.convert_ms_to_hms(time.ticks_ms())
		(11, 38, 15, 650)

.. function:: isEnableWIFI()

	是否启用 WIFI ，系统内部函数。
	
.. function:: isEnableBluetooth()

	是否启用蓝牙，系统内部函数。

.. function:: enableBluetooth()

	启用蓝牙，是系统内部逻辑函数。
	
.. function:: disableBluetooth()

	禁用蓝牙，是系统内部逻辑函数，一般没有用，内核代码限制。

.. function:: enableWIFI()

	启用WIFI，是系统内部逻辑函数。创建一个 wifi 实例，并放在全局变量中，方便程序全局访问。

.. function:: disableWIFI()

	禁用WIFI，从全局变量中禁用 wifi 并释放。

.. function:: delete_folder(folder)

	删除一个空或者非空文件夹下的子目录以及文件。

	* ``folder`` -- 文件夹路径
	
.. function:: gc_collect()

	调用 `gc.collect()` 反复清理内存，让清理彻底。返回清理之后的可以内存。
	
.. function:: compare_and_clean_modules(imported_not_modules[, KEEP_MODULES])

	比较现在已经导入的模块，通过比较 `imported_not_modules` 而后清理多余加载的模块。
	
	* ``imported_not_modules`` -- 没有加载的模块列表，用于比较。
	* ``KEEP_MODULES`` -- 要保留的模块列表。
	

.. function:: debug(g, l[, None])

	变量监控与调试工具。

	* ``g`` -- 全局变量
	* ``l`` -- 局部变量
	* ``v`` -- 额外传入的变量，用于监控变量

	使用方法::

		from TaoLiSystem.core import utils

		a = input("你好！皮卡丘：")
		a = utils.debug(globals(), locals(), a)

		print(a)

	代码输出:

	|

	.. image:: ../_static/core_utils.png
	   :align: center

	|

	.. note:: 注意直接执行 ``exe a=10`` 并不会将原代码中的a值改变，因为函数内的变量表与原代码的变量表是相互隔离的。
	
.. function:: lightsleep_irc([tip, callback])

	让系统进入浅度睡眠，睡眠后按下 A 键进行按键中断唤醒。浅度睡眠可以节约系统资源。
	使用 `button_a.__pin.irq(trigger=Pin.WAKE_LOW, wake=machine.PIN_WAKE)` 设置回调，之后还原。
	
	* ``tip`` -- 是否启用提示，如果为 True ，则会弹出 “已从浅度睡眠中唤醒” 的提示框。
	* ``callback`` -- 在唤醒之后执行的函数，因为唤醒之后可能会导致程序代码次序执行问题，故设置了回调。
	
.. function:: deepsleep_irc()

	让系统进入深度睡眠，睡眠后按下 A 键进行按键中断唤醒。深度睡眠非常节约系统资源，但是唤醒后直接重启掌控板。
	使用 `button_a.__pin.irq(trigger=Pin.WAKE_LOW, wake=machine.PIN_WAKE)` 设置回调。

	
