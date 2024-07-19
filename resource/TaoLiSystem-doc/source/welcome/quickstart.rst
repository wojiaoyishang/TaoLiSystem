安装桃丽系统
================

本章节将介绍如何下载并安装桃丽系统，为了让各位同学都可以方便地安装此系统，所以我将会分布罗列方法。

准备材料
--------

我们需要用到如下的硬件/软件：

* 掌控板、数据线
* mPython IDE（后文将给出下载地址）
* `Thonny IDE <https://thonny.org/>`_ （请自行下载安装）

安装驱动与烧录固件
~~~~~~~~~~~~~~~~~~

完整的安装驱动与烧录固件过程请参考官方文档的 `驱动下载 <https://mpython.readthedocs.io/zh-cn/master/board/drive.html>`_ 和 `烧录固件 <https://mpython.readthedocs.io/zh-cn/master/board/flashburn.html>`_ 章节。

我们使用一种最简单的方法来完成这一步，打开 `盛思官方网站 <https://www.labplus.cn/software>`_ 下载 mPython IDE 并安装。

|

.. image:: ../_static/welcome_mPython-IDE-download.png
   :align: center

|

安装过程中会自动安装掌控板所需的驱动，等待安装完成，打开软件并用数据线连接掌控板，接下来我们需要为掌控板刷固件。

**如果您的掌控板连接上电脑的一瞬间有在oled显示mPython的图标，说明您的掌控板已经内置了固件可以跳过下面的步骤。**

打开 mPython IDE 之后，点击上方的“未连接”的字样，并点击“连接COMX”（X指数字，当您的电脑上有多个掌控板时数字会不一样）。

|

.. image:: ../_static/welcome_mPython-IDE-connect.png
   :align: center

|

如果您的并没有“连接COMX”的字样，请换切换串口连接设备（换一个USB口插）。如果还不行，请确认数据线是否可以使用（部分充电线没有数据传输功能）。最后如果上述均未错误，请检查掌控板是否损坏。

如果提示连接成功，我们可以进入下一步。依次点击右上角的“设置”->“烧录固件”->“确定”，即可烧录固件。

|

.. image:: ../_static/welcome_mPython-IDE-write.png
   :align: center

|

克隆桃丽系统仓库
----------------

克隆顾名思义就是复制仓库的代码到您自己的电脑上面，打开桃丽系统的开源仓库 `码云 <https://gitee.com/wojiaoyishang/TaoLiSystem/>`_ 或 `github <https://github.com/wojiaoyishang/TaoLiSystem/>`_ 。

下载分支里的内容，（码云需要登录，Github可以不用）

|

.. image:: ../_static/welcome_download-TaoLiSystem.png
   :align: center

|

上传桃丽系统到掌控板
--------------------

打开 Thonny IDE ，点击菜单栏 `Tools（工具）` -> `选项...` ->上方选项卡 `Interpreter（解释器）` -> `选择esp32` -> `选择端口` -> `好的` 。等待 Thonny IDE 连接掌控板。

|

.. image:: ../_static/welcome_Thonny-connect.png
   :align: center

|

连接后您会在左侧看到您电脑的文件（左上）和您掌控板的文件（右下），在左上角找到您刚刚解压文件的地方（tip: 点击左上的蓝字可以选择文件夹），然后选择第一项，按住 Shift 选择最后一项，右键 “Upload to /” 上传到掌控板根目录。

|

.. image:: ../_static/welcome_Thonny-upload.png
   :align: center

|


按下掌控板背后的 “rst” 按键重启掌控板，或者在 Thonny IDE 主页面按下 Ctrl + D 重启掌控板。您就可以进入陶丽系统了。
