#coding=utf-8
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
    turns=0
    waiting=None
status=Status()

def t1i(txt,mode,noreturn=False):
    t1.insert(END,str(txt) if noreturn else str(txt)+'\n',mode)
    t1.see(END)

def worker():
    try:
        if status.waiting:
            if not framework.update_turn(status.waiting,t2.get(1.0,END)[:-1]):
                t1i('结果不正确，请重新输入','error')
                return
            else:
                status.waiting=None
                t2.delete(1.0,END)
                t1i('结果正确，开始获取第 %d 组数据.'%(status.turns+1),'green')
        status.turns+=1
        statusvar.set('第 %d 组数据，正在获取长度 ...'%status.turns)
        r=''.join(framework.get_turn())
        t1i('第 %d 组数据是:'%status.turns,'green')
        t1i(r,'blue')
        t1i('请填入正确的输出，然后按确定按钮','')
        status.waiting=r
        tk.bell()
    except framework.interface.Accepted:
        t1i('','')
        t1i('Accepted!','green')
        statusvar.set('已通过，共有 %d 组数据'%status.turns)

def restart():
    def worker_wrapper():
        try:
            worker()
        except Exception as e:
            t1i('','')
            t1i('未知错误: '+str(e),'error')
            raise
        finally:
            okbtn['command']=restart

    okbtn['command']=None
    t=threading.Thread(target=worker_wrapper)
    t.setDaemon(True)
    t.start()

def init(*_):
    def log1(txt):
        t1i(txt,'blue')
    def log2(txt):
        t1i(txt,'debug',noreturn=True)
    def stat(a,b):
        if a=='length':
            status.length=b
        elif a=='bit':
            statusvar.set('第 %d 组数据，正在获取第 %d / %d 位 ...'%\
                (status.turns,b+1,status.length))

    ojname,_,config=t2.get(1.0,END).partition('\n\n')

    try:
        t1i('正在初始化 %s...'%ojname,'')
        framework.init(ojname,json.loads(config),log1,log2,stat)
    except Exception as e:
        t1i('ERROR: '+str(e)+'\n','error')
    else:
        t2.delete(1.0,END)
        restart()

Label(tk,text='状态').grid(row=0,column=0,pady=5)
Label(tk,textvariable=statusvar).grid(row=0,column=1,sticky='we')

t1=Text(tk,font='Consolas -12',height=20)
t1.grid(row=1,column=0,columnspan=2,sticky='nswe')
sbar1=Scrollbar(tk,orient=VERTICAL,command=t1.yview)
sbar1.grid(row=1,column=2,sticky='ns')
t1['yscrollcommand']=sbar1.set
tk.rowconfigure(1,weight=1)

t1.tag_config('blue',foreground='blue',background='white')
t1.tag_config('green',foreground='black',background='#00FF00')
t1.tag_config('debug',foreground='#777777',background='white')
t1.tag_config('error',foreground='white',background='#FF0000')

t1.insert(END,'输入OJ名称和配置来启动ACFan.\n可用OJ:\n')
t1.insert(END,', '.join(framework.ojs)+'\n','blue')

t2=Text(tk,font='Consolas -13',height=10)
t2.grid(row=2,column=0,columnspan=2,sticky='nswe')
sbar2=Scrollbar(tk,orient=VERTICAL,command=t2.yview)
sbar2.grid(row=2,column=2,sticky='ns')
t2['yscrollcommand']=sbar2.set
tk.rowconfigure(2,weight=1)

t2.insert(END,'(OJ名称)\n\n(配置JSON)')

okbtn=Button(tk,text='确定',command=init)
okbtn.grid(row=3,column=0)

btnframe=Frame()
btnframe.grid(row=3,column=2,columnspan=2,sticky='e',pady=5)
#todo: load & save

mainloop()
