.. _welcome:

欢迎查看帮助文档
=================

欢迎您，查看桃丽系统帮助文档！

何为掌控板
----------

掌控板是创客教育专家委员会、猫友汇、广大一线老师共同提出需求并与创客教育行业优秀企业代表共同参与研发的教具、学具，是一块为教育而生的开源硬件，也是一个公益项目。

|

.. image:: ../_static/welcome_TaoLiSystem_gif.gif
   :align: center

|

mPython掌控板是一块MicroPython微控制器板，它集成ESP32高性能双核芯片，使用当下最流行的Python编程语言，以便您轻松地将代码从电脑传输到掌控板中，从而体验程序创作的无穷乐趣！

关于掌控板的更多信息可以参考 `mPython掌控板文档 <https://mpython.readthedocs.io/>`_ 。顺带一提，上面的GIF是修改自官方的掌控板动态图片的。

何为桃丽系统
------------

桃丽系统是掌控板界面设计的一个方案，旨在将零散的代码汇集起来，便于同学老师编程。将掌控板变成一个确切、功能完善的设备。此系统由以赏独立开发，特献给他高一的信息老师，陶丽老师（顺带一提，并不是百度搜到的那个陶丽老师哦！）。系统开发时参考了大量的文献资料，感谢每一位提供文献的小伙伴！

桃丽系统是完全开源的，在 **码云** 开源地址为：`https://gitee.com/wojiaoyishang/TaoLiSystem <https://gitee.com/wojiaoyishang/TaoLiSystem/>`_ 

在 **Github** 开源地址为：`https://github.com/wojiaoyishang/TaoLiSystem <https://github.com/wojiaoyishang/TaoLiSystem/>`_ 

开发说明
------------

这份文档不仅仅是一份使用说明文档，也是一份开发文档。为了便于您对系统二次开发，您必须熟知一些预备知识。这些知识都可以在 `mPython掌控板文档 <https://mpython.readthedocs.io/>`_ 中得知，下面的知识点可以便于您快速入门开发。

* 掌控板基于 ESP32 开发板开发，并以 micropython 语言为基础，经过简单修改后作为掌控板的默认编程语言（也可以称为 mPython 语言）。所以部分资料可以通过添加关键词 “micropython esp32” 来查询。
* 掌控板重新定义了 ESP32 开发板的引脚，部分引脚作为内部硬件使用。引脚的重定义可以参考官方的 `硬件概述 <https://mpython.readthedocs.io/zh/master/board/hardware.html>`_ ，内部硬件使用硬件情况可以查看官方的 `掌控板原理图 <https://mpython.readthedocs.io/zh/master/_downloads/acc90a174707bea8bb175a84ad2f9393/%E6%8E%8C%E6%8E%A7%E6%9D%BF-V2.0.3.pdf>`_ 。
* 掌控板的比较底层硬件编写可以在 `mPython 语言开源仓库 <https://github.com/labplus-cn/mpython>`_ 的 port/boards/mpython 目录找到。
* 在 `mPython 语言开源仓库 <https://github.com/labplus-cn/mpython>`_ 的 port/modules 目录中有掌控板自带的一些模块，大部分没有在 `mPython掌控板文档 <https://mpython.readthedocs.io/>`_ 公开，需要自行查看（因为文档是向重要、实用的方向编写的，一部分冷门模块没有提及）。

其它开源项目
------------

* 新 mpython 图片存储 bin 文件。-> `跳转到mpython图片存储 <https://gitee.com/wojiaoyishang/new-mpython-bin-to-picture>`_ <-
* mpython ili934x - xpt2046 TFT 屏幕驱动。-> `跳转到TFT屏幕驱动 <https://gitee.com/wojiaoyishang/mpython-tft-ili934x-driver>`_ <-


版权说明
------------

此系统在 **码云** 和 **Github** 开源平台上开源，由于精力有限，欢迎大家在开源仓库上指点批评。系统开发采用 **MulanPSL-2.0** 许可证。同时，此系统不可用于商业活动，仅作为个人和公益使用，严禁随意以不正当、不明确理由贩卖。任何以此项目衍生的项目需要尽可能一并开源。
