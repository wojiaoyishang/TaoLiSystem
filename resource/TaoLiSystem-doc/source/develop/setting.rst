设置界面的调用
==============

设置界面不同于主界面，它更像是一个选择器。给用户展示选项，选择，执行。这个章节将简单阐述设置界面的工作原理。

设置页面源代码存储在 `TaoLiSystem/page/setting.py` 中，详细设置项源代码存储在 `TaoLiSystem/page/settingFun.py` 中。

设置项的存储
------------

所有设置项在 `setting.py` 中的 ``settings`` 列表中，列表应该会类似如下这样：

.. code-block:: python

	# 设置项对应设置
	settings = [["无线网络选项", "调整互联网设置", 0, 'wifi_setting'],
                    ["日期时间选项", "调整日期时间", 78, 'date_setting'],
                    ["掌控板选项", "设定掌控板偏好", 184, 'system_setting']]
					
列表 ``settings`` 各项的小项解释如下：

* 第一项为设置项名称。
* 第二项为设置项的简短介绍。
* 第三项为设置项的图标在 `TaoLiSystem/static/setting.bin` 中的位置。图标 bin 文件生成 -> `跳转 <https://gitee.com/wojiaoyishang/new-mpython-bin-to-picture>`_ 。
* 第四项为设置项在 `settingFun.py` 中的函数名称，用户长按触摸 P 按键后调用。

.. note:: 设置项图标大小为 32x32 。

界面逻辑
--------

加入设置界面后，设计界面会重新定义按键中断，并记录 `main.py` 的按键中断。在设置界面到底时，按下 B 键，按键中断还原，并手动调用 B 键中断函数，触发 `main.py` 的页面切换逻辑。部分代码如下：

.. code-block:: python

    # 按钮事件
    def button_b_callback(_):
        global setting_id
        if setting_id == 0:
            setting_id = -1
            button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o  # 还原按钮绑定
            button_b.event_pressed(0)
            return
        setting_id = max(0, setting_id - 1)

在调用设置界面的 ``show()`` 函数时，会进入设置页面的自代码循环，直接在 ``show()`` 循环不退出了。您会在代码中看到这样一句代码：

.. code-block:: python

    _ = setting_id
    # 等待按钮事件
    while _ == setting_id:   # 改变说明按键中断，改变了 setting_id 的值
        # 其它代码
		
代码中的 ``setting_id`` 是全局变量，在进入循环前，把值赋给了 ``_`` 这个局部变量，然后使用看似“死条件”的 ``_ == setting_id`` 来循环。实际上，正是因为 ``setting_id`` 是全局变量，而我们又设置了按键中断，当用户按下按键时，程序被中断了，转而去执行按钮事件函数 ``button_X_callback()`` （X 代表 a 或 b），在函数中会改变 ``setting_id`` 的值，使循环条件不成立跳出循环，转而让 ``show()`` 执行结束。在 `main.py` 再次调用 ``show()`` 按照新的 ``setting_id`` 绘制新的设置项。

这个写法在插件界面中也有出现。