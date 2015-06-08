#coding=utf-8
import sys
assert sys.version[0]!='2', 'Please Use Python3'

import OJInterface as interface
import json

ojs=interface.valid_ojs
killed=False

known_turns=[]
known_bytes=[]
dataver='log2'

class OJWrapper:
    ojs=[]
    ind=0
    
    def __init__(self,OJClass,configs,log2):
        for config in configs:
            self.ojs.append(OJClass(log2,config))
        self.len_ojs=len(self.ojs)
        log('用户池中有 %d 个登录凭据'%self.len_ojs)
    
    def update(self,source):
        if killed:
            raise interface.Error('任务中断')
        
        self.ind=(self.ind+1)%self.len_ojs
        return self.ojs[self.ind].update(source)

def init(oj_name,configs,log1=print,log2=lambda a:print(a,end=''),stat_function=lambda *_:None):
    global log
    global oj
    global stat
    
    log=log1
    stat=stat_function

    if not isinstance(configs,(tuple,list)):
        configs=[configs]
    oj=OJWrapper(interface.valid_ojs[oj_name],configs,log2)
    
    if __name__=='__main__':
        print('初始化完成')
        print('输入 cli() 来开始')
        print('输入 save() 来保存进度，输入 load(config) 来读取进度')

base_code='''
#include<cstdio>
#include<cstring>
unsigned int p=0;
void WA(){printf("this_is_absolutely_a_wrong_answer_2333");}
void TLE(){while(1);}
void MLE(){while(1)new long long;}
void RE(){throw;}
void OLE(){while(1)printf("i_am_a_junk_string_isnt_it");}
bool OK(char *a,char *b){if(p!=strlen(b))return false;
for(unsigned int x=0;x<strlen(b);x++)if(a[x]!=b[x])return false;
return true;}
int main(){
char i[625];while(scanf("%c",i+p)!=EOF)p++;
[BASE]
return 0;}'''

len_code='''
if(p<%d)WA();
else if(p<%d)TLE();
else if(p<%d)MLE();
else if(p<%d)RE();
else OLE();
'''

bit_code='''
if(i[[IND]]<%d)WA();
else if(i[[IND]]<%d)TLE();
else if(i[[IND]]<%d)MLE();
else if(i[[IND]]<%d)RE();
else OLE();
'''

whitelist_code='''
if(OK(i,(char*)"[DATA]")){printf("%s","[OUTPUT]");return 0;}
[BASE]'''

def get_len():
    log('获取长度...')
    i,j=0,125
    while j>=1:      
        r=oj.update(base_code.replace('[BASE]',\
            len_code%(i+j,i+2*j,i+3*j,i+4*j)))
        i,j=i+r*j,j//5
    if i>=624:
        raise interface.Error('长度过长.')
    else:
        global known_bytes
        known_bytes=[None for _ in range(i)]
        return i
    
def get_bit(ind):    
    log('获取第 %d 位...'%(ind+1))
    i,j=0,25
    while j>=1:      
        r=oj.update(base_code.replace('[BASE]',\
            (bit_code%(i+j,i+2*j,i+3*j,i+4*j)).replace('[IND]',str(ind))))
        i,j=i+r*j,j//5

    known_bytes[ind]=chr(i)
    return i

def update_turn(data,output):
    def whitelist(data,output):
        def trim(x):
            return x.replace('"',r'\"').replace('\t',r'\t').replace('\n',r'\n')
        return base_code.replace('[BASE]',whitelist_code.\
            replace('[DATA]',trim(data)).replace('[OUTPUT]',trim(output)))

    log('正在检验输出...')
    result=oj.update(whitelist(data,output).replace('[BASE]','TLE();'))
    if result==1:
        global base_code
        base_code=whitelist(data,output)
        known_turns.append([data,output])
        global known_bytes
        known_bytes=[]
        stat('turn',None)
        return True
    else:
        return False

def get_turn():
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
            result[now]=chr(get_bit(now))
        log('第 %d 位是 %s(%d)'%(now+1,repr(result[now]),ord(result[now])))
    return result

def save():
    return json.dumps({
        'known_turns':known_turns,
        'dataver':dataver,
        'known_bytes':known_bytes,
    })

def load(config):
    data=json.loads(config)
    if data['dataver']!=dataver:
        log('存档版本无法识别')
        return False
    global known_bytes
    known_bytes=data['known_bytes']
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
                print('第 %d 组数据，正在获取长度 ...'%(len(known_turns)+1))
                r=''.join(get_turn())
                print('输入是\n%s'%r)
                print('请填入正确的输出：')
                while True:
                    #every output
                    try:
                        d=eval(input('[REPR]: '))
                    except Exception as e:
                        print('解析失败: %s'%e)
                    else:
                        if not isinstance(d,(str,bytes)):
                            print('请输入 REPR 格式的字符串')
                        elif update_turn(r,d):
                            print('输出正确')
                            break
                        else:
                            print('输出错误，请重试')
        except interface.Accepted:
            print('Accepted!')
        except interface.Error as e:
            print('接口错误: %s'%e)
