# ACFan
自动AC机，刷OJ必备~

目前原生兼容POJ和HustOJ，支持开发其他OJ的扩展接口。

**ACFan的原理解析和适用范围详见[这篇wiki文章](https://github.com/xmcp/ACFan/wiki/ACFan-%E5%8E%9F%E7%90%86%E8%A7%A3%E6%9E%90)**

# Runtime
Python **3.x**

(在 Python 3.4.0 上开发并测试)

# 依赖
- `beautifulsoup4`
- `html5lib`
- `tkinter`

# 用法
ACFan有两个版本：GUI版和命令行版。如果条件允许，**请首先使用GUI版**。

## GUI版本
运行`ACFan.pyw`

出现的窗口中包括两个文本框。上面的浅灰色文本框将输出log信息，虽然你可以在上面输入文字但这并没有什么卵用。**下面的白色文本框才是给你输入信息用的。**

在输入框中输入OJ名称（区分大小写）然后按**两次**回车，接着按照提示输入OJ的配置信息（例如用户名、密码和题号）并按“登录”按钮来完成初始化。

有的OJ对同一账号提交代码的间隔有限制（比如HustOJ的限制是10秒一次），此时你可以把多组配置信息放在一个`JSON Array`里，ACFan将依次用这些账号提交代码,以绕过时间间隔限制。例如：

    [
        {"username":"测试1","password":"测试1","problem":1000},
        {"username":"测试2","password":"测试2","problem":1000},
        {"username":"测试3","password":"测试3","problem":1000}
    ]

初始化完毕后，点击“继续”按钮开始自动化dump。

对于数据量较大的题目，dump可能会花一段时间，你随时可以在暂停后按“保存”按钮保存当前进度。点击“保存”按钮后，“存档字符串”会出现在输入框中，**把它复制到别的地方并妥善保存**。当你想读取存档时，将存档字符串粘贴到输入框中，然后按“读取”。

在自动化dump过程中，你需要按照屏幕上的提示，手算出每一组输入数据的正确输出。ACFan会检验您的答案是否正确。

## 命令行版本

运行`ACFramework.py`，然后按照屏幕提示进行操作。

***注意：请在交互shell（使用`-i`命令行参数），或在IDLE中运行，不要双击或在cmd中直接运行。***

***注意：在交互shell中默认有输出缓存，所以log可能在不换行时不更新，添加 `-u` 命令行参数来禁用输出缓存。如果你搞不定输出缓存的事，建议你在IDLE中打开`ACFramework`并运行。***

# 扩展OJ接口
目前ACFan仅兼容POJ和HustOJ（大视野测评使用的是HustOJ）。如果你想让ACFan兼容其它OJ，你可以自己动手写一个接口。

方法如下：

### 首先用文本编辑器打开 `OJInterface.py`，创建一个类（名称随意）。

### 然后为这个类实现以下方法或属性：

- **`__init__(self, log, config)`**

在这个方法中初始化你的接口（例如：试图登录OJ并保存登录凭据共以后使用）

参数`log`是个函数，它接收一个`str`并将其输出。为了让GUI用户看着爽，你应该用`log`输出调试信息而不是`print`。

***注意：*** `log`**不会**在字符串末尾为你添加换行符。所以请在需要换行的地方自己加'\n'。

当初始化的时候，`config`参数会被传入。你可以把它存下来（如果后面需要的话）。`config`的类型取决于用户的输入*，但是强烈推荐使用字典类型。

\* *对于命令行界面，用户想传什么config就传什么；对于图形界面，你收到的`config`是`JSON.loads`过的用户输入。*

如果有什么意外（比如密码错误），你应当`raise Error(字符串格式的原因)`

- **`update(self, source)`**

在此方法中，你将`source`提交到OJ并返回判题结果。
五个结果(WA, TLE, MLE, RE, OLE)已经在`OJInterface.py`的顶部定义了。

比如说如果OJ的判题结果是`Runtime Error`，你应当`return RE`。

对于`Accepted`结果，直接`raise Accepted()`；
对于`Compile Error`，抛出一个Error吧；
对于`Presentation Error`（如有），官方的建议是先用log提示一下用户，然后`return WA`。

你的代码应该考虑到OJ的反垃圾系统。再重申一遍，如果有什么异常，`raise Error(reason)`。

鉴于OJ判题需要一段时间，你可以在取得一定进展时用`log`告诉用户，以免用户等不及。

- **`default_var`**

这是一个字符串，它解释了用户应该在`__init__`的`config`参数里填什么。
这个属性是针对GUI用户的，所以你要确定`default_var`是合法的JSON。

### 最后，翻到文件底部，在`valid_ojs`字典里加上你的OJ接口。
格式是：`{'你的OJ名称': Your_OJ_Class}`

### 贯彻开源精神
欢迎以 pull request 的方式为 ACFan 贡献你的接口。

# License

*This program is free software. It comes without any warranty, to the extent permitted by applicable law. You can redistribute it and/or modify it under the terms of the Do What The Fuck You Want To Public License, Version 2, as published by Sam Hocevar. See below for more details.*

                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                        Version 2, December 2004
    
     Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
    
     Everyone is permitted to copy and distribute verbatim or modified
     copies of this license document, and changing it is allowed as long
     as the name is changed.
    
                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
    
      0. You just DO WHAT THE FUCK YOU WANT TO.
