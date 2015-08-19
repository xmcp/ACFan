# ACFan
自动AC机，刷OJ必备~

兼容POJ和HustOJ。

**ACFan的原理解析和适用范围详见[这篇wiki文章](https://github.com/xmcp/ACFan/wiki/ACFan-%E5%8E%9F%E7%90%86%E8%A7%A3%E6%9E%90)**

#Runtime
Python **3.x**

(在 Python 3.4.0 上开发并测试)

#依赖包
- `beautifulsoup4`
- `html5lib`

可以用`pip install`安装

#用法
GUI版本：运行`ACFan.pyw`

命令行版本：运行`ACFramework.py` ***(注意：请在交互shell，比如IDLE中运行，不要双击或在cmd中直接运行)***

# 自定义
目前ACFan仅兼容POJ和HustOJ（大视野测评使用的就是HustOJ）。如果你想让ACFan兼容其它OJ，你可以自己动手写一个接口。

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
