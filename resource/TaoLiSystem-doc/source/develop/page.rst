界面开发与主循环调用
====================

系统中有三大界面：主界面、设置界面、插件界面。与其它页面不同的是，它们是直接由 `main.py` 循环调用的。

这些界面存在于目录 `TaoLiSystem/page` 文件夹下，并在 `main.py` 代码中做了登记，查看 `main.py` 文件，您可以找到下面这段代码：

.. code-block:: python
	
	# 全部页面模块
	pages = ["TaoLiSystem.page.setting", "TaoLiSystem.page.home", "TaoLiSystem.page.plugin"]
	page_id = 1  # 当前页面
	
主循环调用
----------

系统有一个主循环，用来维持系统不会被意外代码终止而意外退出。此代码存在于 `main.py` 中，但 `main.py` 没有界面绘制的能力（没有在 `main.py` 中直接绘制主界面，为了面向对象，明确各个代码的分工。），所以就调用 ``pages`` 变量里的模块来绘制。注：pages并未直接导入上面的模块，而是根据提供的字符串来动态导入模块。

比如按照上述代码，系统会调用 `TaoLiSystem.page.home` 模块中的 ``show()`` 函数来绘制，这个是代码预先规定好的。

页面加载、退出的逻辑由 `main.py` 引导，当切换页面时（按下 A 键或 B键）， `main.py` 会等待界面模块中 ``show()`` 函数执行完毕，再调用界面模块中的 ``close()`` 函数。在 ``close()`` 函数执行完毕之后， `main.py` 会清理界面模块本身以及其导入的其它模块，清理结束后调用其它界面模块。

.. note:: 模块的导入与删除，参照 `main.py` 文件中的，``importModule()`` 函数和 ``close_module()`` 函数。

界面代码设计
------------

界面是允许动态插入与更新的，您可以自己写一个界面并插入到 `main.py` 页面模块列表之中。但是最好插入在 `TaoLiSystem.page.setting` 之后，或者 `TaoLiSystem.page.plugin` 之前，因为这两个界面是系统的“边界”。

假设我新建了一个 `testUI.py` 在 `TaoLiSystem/page` 文件夹下，您必须至少在 `testUI.py` 中包含如下内容：


.. code-block:: python

    def show():
        # main.py 会反复调用这个函数
        pass

    def close():
        # 界面关闭时，会先调用这里。
        pass

然后在 `main.py` 的 ``pages`` 列表中插入 ``TaoLiSystem.page.testUI`` ，如下：

.. code-block:: python

	# 全部页面模块
	pages = ["TaoLiSystem.page.setting", "TaoLiSystem.page.home", "TaoLiSystem.page.testUI", "TaoLiSystem.page.plugin"]
	page_id = 1  # 当前页面

然后重启掌控板，按下 B 键，就会进入到 `testUI.py` 中 ``show()`` 函数中了。

.. important:: 

	* 因为界面的模块是动态导入与动态释放的，所以模块中的所有代码都会在导入的时候再次执行，不必当心重复导入代码不执行的问题。
	* 界面的按键判断是通过 `按键中断 <https://mpython.readthedocs.io/zh/master/tutorials/basics/buttons.html>`_ 的，所以即使界面模块销毁，按键 A 或 按键 B 的按下事件仍会触发。

你可以通过下面的代码暂时禁止 `main.py` 设置的按键中断：

.. code-block:: python

	# 记录原本按钮绑定函数
	button_a_callback_o, button_b_callback_o = button_a.event_pressed, button_b.event_pressed
	button_a.event_pressed, button_b.event_pressed = None, None

	# do something......

	# 还原按键中断
	button_a.event_pressed, button_b.event_pressed = button_a_callback_o, button_b_callback_o
