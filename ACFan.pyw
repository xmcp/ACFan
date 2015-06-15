#coding=utf-8
import sys
if sys.version[0]=='2':
    from Tkinter import Tk,mainloop,Label
    tk=Tk()
    tk.title('错误')
    Label(tk,text='ACFan 需要使用 Python3.').pack(padx=20,pady=10)
    mainloop()
    sys.exit(-1)

import ACFramework as framework
from tkinter import *
from tkinter.ttk import *
import threading
import json

tk=Tk()
tk.title('ACFan')
tk.columnconfigure(1,weight=1)
tk.geometry('600x500')

statusvar=StringVar()
statusvar.set('就绪')

class Status:
    length=0
    turns=1
    waiting=None
    mode=None
status=Status()

def t1i(txt,mode,noreturn=False):
    t1.insert(END,str(txt) if noreturn else str(txt)+'\n',mode)
    t1.see(END)

def worker():
    try:
        if status.waiting:
            if not framework.update_turn(status.waiting,t2.get(1.0,END)[:-1],status.mode):
                t1i('结果不正确，请重新输入','error')
                return
            else:
                status.waiting=None
                t2.delete(1.0,END)
                status.turns+=1
                t1i('结果正确，正在继续运行','blue')
                
        statusvar.set('第 %d 组数据 ...'%status.turns)
        r,_=framework.get_turn()
        t1i('第 %d 组数据是:'%status.turns,'green')
        t1i(r,'blue')
        t1i('请填入正确的输出，然后按确定按钮','')
        status.waiting=r
        statusvar.set('第 %d 组数据，输入已获取，等待填入输出 ...'%status.turns)
        tk.focus_force()
    except framework.interface.Accepted:
        t1i('','')
        t1i('Accepted!','green')
        statusvar.set('已通过，共有 %d 组数据'%status.turns)
    except framework.interface.Error as e:
        t1i('','')
        t1i('错误: '+repr(e),'error')

def restart():
    def worker_wrapper():
        try:
            framework.killed=False
            loadbtn['state']='disabled'
            worker()
        except Exception as e:
            t1i('','')
            t1i('未知错误: '+repr(e),'error')
            raise
        finally:
            okbtn['command']=restart
            okbtn['text']='继续'
            okbtn['state']='normal'
            loadbtn['state']='normal'

    def kill(*_):
        framework.killed=True
        okbtn['text']='正在停止……'
        okbtn['state']='disabled'

    okbtn['command']=kill
    okbtn['text']='停止'
    t=threading.Thread(target=worker_wrapper)
    t.setDaemon(True)
    t.start()

def load(*_):
    def async_load(data):
        try:
            framework.killed=False
            assert framework.load(data), '进度读取失败'
        except Exception as e:
            t1i('错误: %s'%repr(e),'error')
            loadbtn['state']='normal'
        else:
            t1i('进度读取成功','green')
            t2.delete(1.0,END)
            restart()
        finally:
            okbtn['state']='normal'
    
    okbtn['state']='disabled'
    loadbtn['state']='disabled'
    statusvar.set('正在读取进度 ...')
    data=t2.get(1.0,END)[:-1]
    t=threading.Thread(target=async_load,args=(data,))
    t.setDaemon(True)
    t.start()

def save(*_):
    try:
        data=framework.save()
    except Exception as e:
        t1i('错误: %s'%repr(e),'error')
    else:
        t2.delete(1.0,END)
        t2.insert(END,data)

def init(*_):
    def log1(txt):
        t1i(txt,'blue')
    def log2(txt):
        t1i(txt,'debug',noreturn=True)
    def stat(a,b):
        if a=='length':
            status.length=b
        elif a=='bit':
            statusvar.set('第 %d 组数据，%s 字符集，正在获取第 %d / %d 位 ...'%\
                (status.turns,status.mode,b+1,status.length))
        elif a=='turn':
            status.turns+=1
        elif a=='mode':
            status.mode=b
            statusvar.set('第 %d 组数据，%s 字符集，正在获取长度 ...'%\
                (status.turns,b))
        else:
            log('警告: stat收到了未知的回调参数 '+repr((a,b)),'error')

    ojname,_,config=t2.get(1.0,END).partition('\n\n')

    try:
        t1i('正在初始化 %s...'%ojname,'')
        framework.init(ojname,json.loads(config),log1,log2,stat)
    except Exception as e:
        t1i('错误: '+repr(e),'error')
    else:
        t2.delete(1.0,END)
        t2.unbind('<Return>')
        okbtn['command']=restart
        okbtn['text']='继续'
        loadbtn['state']='normal'
        t1i('填入存档字符串来并点击“读取”从存档开始，点击“继续”开始新的任务','')
    
def enter_callback(*_):
    if t2.index(INSERT).startswith('2.'):
        ojname=t2.get('1.0','2.0').rstrip()
        if ojname not in framework.ojs:
            t1i('错误的OJ名称','error')
        else:
            t2.delete('3.0',END)
            try:
                t2.insert('3.0','\n'+framework.ojs[ojname].default_var)
            except AttributeError:
                t1i('无法获取 %s 的默认参数','error')
    
Label(tk,text='状态').grid(row=0,column=0,pady=5)
Label(tk,textvariable=statusvar).grid(row=0,column=1,sticky='we')

T1BG='#dddddd'
t1=Text(tk,font='Consolas -12',bg=T1BG,height=20)
t1.grid(row=1,column=0,columnspan=2,sticky='nswe')
sbar1=Scrollbar(tk,orient=VERTICAL,command=t1.yview)
sbar1.grid(row=1,column=2,sticky='ns')
t1['yscrollcommand']=sbar1.set
tk.rowconfigure(1,weight=3)

t1.tag_config('blue',foreground='blue',background=T1BG)
t1.tag_config('green',foreground='black',background='#00FF00')
t1.tag_config('debug',foreground='#777777',background=T1BG)
t1.tag_config('error',foreground='white',background='#FF0000')

t1.insert(END,'输入OJ名称和配置（以空行分隔）来启动ACFan.\n可用OJ列表:\n')
t1.insert(END,', '.join(framework.ojs)+'\n','blue')

t2=Text(tk,font='Consolas -13',height=10)
t2.grid(row=2,column=0,columnspan=2,sticky='nswe')
sbar2=Scrollbar(tk,orient=VERTICAL,command=t2.yview)
sbar2.grid(row=2,column=2,sticky='ns')
t2['yscrollcommand']=sbar2.set
tk.rowconfigure(2,weight=1)

t2.bind('<Return>',enter_callback)

okbtn=Button(tk,text='登录',command=init)
okbtn.grid(row=3,column=0)

btnframe=Frame()
btnframe.grid(row=3,column=1,columnspan=2,sticky='e')

loadbtn=Button(btnframe,text='读取',state='disabled',command=load)
loadbtn.grid(row=0,column=0,padx=5)
Button(btnframe,text='保存',command=save).grid(row=0,column=1,padx=5)

tk.bind('<F5>',lambda *_:okbtn.invoke())
mainloop()
