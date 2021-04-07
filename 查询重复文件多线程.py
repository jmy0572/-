import os,hashlib,sys,time,gevent
from collections import Counter
from gevent import monkey
from gevent.queue import Queue

monkey.patch_all()
work=Queue()
def find(dict1,value1):
    list1=[]
    first_pos = 0
    for i in range(dict1.count(value1)):
        new_list = dict1[first_pos:]
        next_pos = new_list.index(value1) + 1
        list1.append(first_pos + new_list.index(value1))
        first_pos += next_pos
    return list1
list1=[]
listurl=[]
loading=1
list2=[]
listgevent=[]
path = r'./'
# path=r''+input(r'请输入需要查询重复文件的文件夹地址 如C:\Users\Administrator'+'\n')
# if '‪' in path:
#     path=path.replace('‪','')   #删除windows盘符前的特殊符号
start = time.time()
filenames = os.listdir(path)
for i in filenames:
    if '.' not in i:
        continue
    nameurl = path+'\\' + i
    list1.append(i)
    listurl.append(nameurl)
for i in listurl:
    work.put_nowait(i)

def listwait():
    while not work.empty():
        filename=work.get_nowait()
        global loading
        print(f'正在处理第{loading}个文件    已用时间:{time.time()-start:.2f}秒',end='\r')
        loading=loading+1
        fp=open(filename,'rb')
        contents=fp.read()
        fp.close()
        a=hashlib.md5(contents).hexdigest()
        list2.append(a)
for i in range(4):
    t=gevent.spawn(listwait)
    listgevent.append(t)
gevent.joinall(listgevent)
a222=dict(Counter(list2))
aa=[key for key,value in a222.items() if value > 1]
for i in aa:
    cc=find(list2,i)
    for num in cc:
        print(list1[num],end=' || ')
    print(':',i,'\n')
end=time.time()
print(f'共检测文件{loading}个,用时{end-start:.2f}秒')
input('按任意键退出')