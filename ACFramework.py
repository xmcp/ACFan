#coding=utf-8
import sys
assert sys.version[0]!='2', 'Please Use Python3'

import OJInterface as interface
import json

ojs=interface.valid_ojs
killed=False

known_turns=[]
known_bytes=[]
current_mode=None
dataver='log3'

class OJWrapper:
    ojs=[]
    ind=0
    
    def __init__(self,OJClass,configs,log2,_refresh):
        for config in configs:
            self.ojs.append(OJClass(log2,config))
            _refresh()
        self.len_ojs=len(self.ojs)
        log('用户池中有 %d 个登录凭据'%self.len_ojs)
    
    def update(self,source):
        if killed:
            raise interface.Error('任务中断')
        
        try:
            return self.ojs[self.ind].update(source)
        finally:
            self.ind=(self.ind+1)%self.len_ojs

def init(oj_name,configs,log1=print,log2=lambda a:print(a,end=''),
        stat_function=(lambda *_:None),refresh_function=(lambda *_:None)):
    global log
    global oj
    global stat
    
    log=log1
    stat=stat_function

    if not isinstance(configs,(tuple,list)):
        configs=[configs]
    oj=OJWrapper(interface.valid_ojs[oj_name],configs,log2,refresh_function)
    
    if __name__=='__main__':
        print('初始化完成')
        print('输入 cli() 来开始')
        print('输入 save() 来保存进度，输入 load(config) 来读取进度')

base_code='''
#include<cstdio>
#include<cstring>
#define _C if(unsigned(p)!=strlen(b))return false
int p=0;
void WA(){printf("this_is_absolutely_a_wrong_answer_2333");}
void TLE(){while(1);}
void MLE(){while(1)new long long[233333];}
void RE(){throw;}
void OLE(){while(1)printf("i_am_a_junk_string_isnt_it");}
bool OKfull(char *a,char *b){_C;
for(int x=0;x<p;x++)if(a[x]!=b[x])return false;
return true;}
bool OKnorm(char *a,char *b){_C;
for(int x=0;x<p;x++){if((a[x]>96&&a[x]<123?a[x]-32:a[x])!=b[x])return false;}
return true;}
bool OKlite(char *a,char *b){_C;
for(int x=0;x<p;x++){if((a[x]=='\\n'?' ':a[x])!=b[x])return false;}
return true;}
int main(){
char i[625];while(scanf("%c",i+p)!=EOF)if(i[p]!='\\r')p++;i[p]='\\0';
//BASE
return 0;}'''

mode_code='''
char norm[]="0123456789 \\nX+-*/=.ABCDEFabcdef",lite[]="0123456789 \\n";
bool nf=1,lf=1;
for(int x=0;x<p;x++){if(nf&&strchr(norm,i[x])==NULL)nf=0;if(lf&&strchr(lite,i[x])==NULL)lf=0;}
if(!nf)WA();
else if(!lf)TLE();
else if(p<625)MLE();
else OLE();'''

len_code='''
if(p<%d)WA();
else if(p<%d)TLE();
else if(p<%d)MLE();
else if(p<%d)RE();
else OLE();
'''

bit_code_full='''
if(i[[IND]]<%d)WA();
else if(i[[IND]]<%d)TLE();
else if(i[[IND]]<%d)MLE();
else if(i[[IND]]<%d)RE();
else OLE();
'''

bit_code_norm='''
char *u="0123456789 \\nX+-*/=.ABCDEF",
*r=strchr(u,(i[[IND]]>96&&i[[IND]]<123?i[[IND]]-32:i[[IND]]));
if(r-u<%d)WA();
else if(r-u<%d)TLE();
else if(r-u<%d)MLE();
else if(r-u<%d)RE();
else OLE();
'''

bit_code_lite='''
char *u="0123456789 ",
*r1=strchr(u,(i[[IND]]=='\\n'?' ':i[[IND]])),
*r2=([IND]+1==p?u+10:strchr(u,(i[[IND]+1]=='\\n'?' ':i[[IND]+1])));
int r=(r1-u)*11+(r2-u);
if(r<%d)WA();
else if(r<%d)TLE();
else if(r<%d)MLE();
else if(r<%d)RE();
else OLE();
'''

whitelist_code='''
if(OK[MODE](i,(char*)"[DATA]")){printf("%s","[OUTPUT]");return 0;}
//BASE'''

def get_mode():
    log('选择最佳模式...')
    r=oj.update(base_code.replace('//BASE',mode_code))
    if r==interface.RE:
        raise interface.Error('意外的运行时错误')
    elif r==4:
        raise interface.Error('数据量过大')
    else:
        global current_mode
        current_mode={0:'full', 1:'norm', 2:'lite'}[r]
        return current_mode

def get_len():
    log('获取长度...')
    i,j=0,125
    while j>=1:      
        r=oj.update(base_code.replace('//BASE',\
            len_code%(i+j,i+2*j,i+3*j,i+4*j)))
        i,j=i+r*j,j//5
    global known_bytes
    known_bytes=[None for _ in range(i)]
    return i
    
def get_bit(ind,mode):    
    log('获取第 %d 位...'%(ind+1))
    if mode=='full':
        i,j=5,25
        while j>=1:
            r=oj.update(base_code.replace('//BASE',\
                (bit_code_full%(i+j,i+2*j,i+3*j,i+4*j)).replace('[IND]',str(ind))))
            i,j=i+r*j,j//5
        result=chr(i)
        known_bytes[ind]=result
    elif mode=='norm':
        i,j=0,5
        while j>=1:
            r=oj.update(base_code.replace('//BASE',\
                (bit_code_norm%(i+j,i+2*j,i+3*j,i+4*j)).replace('[IND]',str(ind))))
            i,j=i+r*j,j//5
        result='0123456789 \nX+-*/=.ABCDEF'[i]
        known_bytes[ind]=result
    elif mode=='lite':
        length=len(known_bytes)
        i,j=0,25
        di='0123456789 '
        while j>=1:
            r=oj.update(base_code.replace('//BASE',\
                (bit_code_lite%(i+j,i+2*j,i+3*j,i+4*j)).replace('[IND]',str(ind))))
            i,j=i+r*j,j//5
        result=di[i//11]
        known_bytes[ind]=result
        if ind+1!=length:
            known_bytes[ind+1]=di[i%11]
    else:
        raise interface.Error('错误的模式')
    return result

def update_turn(data,output,mode):
    def whitelist(data,output,mode):
        def trim(x):
            return x.replace('"',r'\"').replace('\t',r'\t').replace('\n',r'\n')
        return base_code.replace('//BASE',whitelist_code.\
            replace('[DATA]',trim(data)).replace('[OUTPUT]',trim(output))\
                .replace('[MODE]',mode))

    log('正在检验输出...')
    result=oj.update(whitelist(data,output,mode).replace('//BASE','TLE();'))
    if result==1:
        global base_code
        base_code=whitelist(data,output,mode)
        known_turns.append([data,output,mode])
        global known_bytes
        known_bytes=[]
        global current_mode
        current_mode=None
        stat('turn',len(known_turns))
        return True
    else:
        return False

def get_turn():
    if current_mode:
        m=current_mode
    else:
        m=get_mode()
    log('使用 %s 字符集'%m)
    stat('mode',m)
    
    if m=='lite':
        log('注意: 在此字符集中，换行符会被视为空格')
    elif m=='norm':
        log('注意：在此字符集中，小写字母会被视为大写字母')
    
    if known_bytes==[]:
        l=get_len()
    else:
        l=len(known_bytes)
    log('长度是 %d'%l)
    stat('length',l)
    
    result=[None for _ in range(l)]
    for now in range(l):
        stat('bit',now)
        if known_bytes[now]:
            result[now]=known_bytes[now]
        else:
            result[now]=get_bit(now,m)
        log('第 %d 位是 %s(%d)'%(now+1,repr(result[now]),ord(result[now])))
    return (''.join(result),m)

def save():
    return json.dumps({
        'known_turns':known_turns,
        'dataver':dataver,
        'known_bytes':known_bytes,
        'current_mode':current_mode,
    })

def load(config):
    data=json.loads(config)
    if data['dataver']!=dataver:
        log('存档版本无法识别')
        return False
    global known_bytes
    global current_mode
    known_bytes=data['known_bytes']
    current_mode=data['current_mode']
    for a in data['known_turns']:
        if not update_turn(*a):
            log('输出不正确: %s'%(a,))
    return True

if __name__=='__main__':
    print('欢迎使用 ACFan (by @xmcp) 命令行')
    print('可用OJ: '+', '.join(ojs.keys()))
    print('在 Python Shell 中输入 init(oj_name,oj_config_or_list_of_configs) 来初始化')
    def cli():
        try:
            while True:
                #every turn
                print('第 %d 组数据，正在选取最佳模式 ...'%(len(known_turns)+1))
                r,mode=get_turn()
                print('输入是\n%s'%r)
                print('请填入正确的输出：')
                while True:
                    #every output
                    try:
                        d=eval(input('[REPR]: '))
                    except Exception as e:
                        print('解析失败: %s'%repr(e))
                    else:
                        if not isinstance(d,(str,bytes)):
                            print('请输入 REPR 格式的字符串')
                        elif update_turn(r,d,mode):
                            print('输出正确')
                            break
                        else:
                            print('输出错误，请重试')
        except interface.Accepted:
            print('Accepted!')
        except interface.Error as e:
            print('接口错误: %s'%repr(e))

