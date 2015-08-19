# ACFan
自动AC机，刷OJ必备~

兼容POJ和HustOJ。

**ACFan的原理解析和适用范围详见[这篇wiki文章](https://github.com/xmcp/ACFan/wiki/ACFan-%E5%8E%9F%E7%90%86%E8%A7%A3%E6%9E%90)**

#Runtime
Python **3.x**

(Tested on Python 3.4.0)

#Requirements
- `beautifulsoup4`
- `html5lib`

#Usage
GUI Version: `ACFan.pyw`

Command Line Version: `ACFramework.py` ***(run it in an interactive shell or IDLE)***

# Configuration
To extend this program, you are welcomed to build the interface of your OJ for ACFan.

See how to build the interface below.

### First, open `OJInterface.py`, and create a class.

### Then implement the following methods and attributes:

- **`__init__(self, log, config)`**

Initialize your interface here.

`log` is a funtion that receives a `str` and print it to the screen.
You should use `log` function instead of `print` for GUI-friendly.

***ATTTENTION: *** `log` DOSEN'T add '\n' after your str. Add it yourself.

While initializing, a `config` parameter will be passed to your interface. Save it for your later use.
`config` can be any type, but *it's recommended to use `dict` type*.

If anything is wrong, `raise Error(reason)`.

- **`update(self, source)`**

Submit the `source` to OJ and return the result.
Five result (WA, TLE, MLE, RE, OLE) is pre-defined in `OJInterface.py`. Take it for granted :)

For `Accepted` result, just `raise Accepted()`.
For `Compile Error`, you should raise an Error.

Your code should handle the anti-spam system of your OJ.
Again, if anything is wrong, `raise Error(reason)`.

Don't forget to log something while submitting the code and querying the result.

- **`default_var`**

It's a `str` that explains what user should use as the `config` paramenter of `__init__`.

### Finally, update the `valid_ojs` dictionary at the bottom of the file.
The format is: `{'your_oj_name': Your_OJ_Class}`
