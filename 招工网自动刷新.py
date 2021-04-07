import time,requests,json,os,random,gevent
from bs4 import BeautifulSoup
os.system("cls")
telephone='13004267812'#电话
workerid='' #编号
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

url="https://www.zlrcsc.com/mobile/company/addemploy.htm" #发布网址
url1='https://www.zlrcsc.com/mobile/members/login.htm' #登录网址
url3="https://www.zlrcsc.com/mobile/company/employ.htm"#后台网址
data1={   #登录账号
        'username': '17195876544',
        'password': 'jian0572',
        'expire': '1'
    }
data2={   #招聘文本
    'cate': '整件缝纫车工机工',
    'wage': '按件计价多劳多得',
    'realname': '简永成',
    'tel': telephone,
    'company': '利达中路 急招整件车工 奇偲宝贝制衣',
    'address': '利达中路226号',
    'content': '女童针织T恤和裙子都做,不是加工厂,已经开工,急招员工,工价高,详谈加我微信或者打给我电话',
    'workerid': workerid
    }
b=0  #刷新职位次数
bb=0#被下架次数
def start():         #账号后台
    r=requests.session()
    print('        登录后台中...')
    c=r.post(url1,headers=headers,data=data1)
    res = r.get(url3)
    c=BeautifulSoup(res.text,'html.parser')
    try:
        global workerid,data2,bb
        workerid=c.find(class_="section-cols clearfix").find('a')['href'][-10:-4]
        print('      读取信息编号成功')
        data2['workerid']=workerid
    except:
        input('   职位被下架,按回车键重新发布')
        data2['workerid']=''
        job()
        bb+=1
def find1():#查找是否刷新成功
    dictTel={}
    url='https://www.zlrcsc.com/mobile/index/index.htm?m=Mobile&c=Index&a=index&key='
    r=requests.get(url)
    c=BeautifulSoup(r.text, 'html.parser')
    c1=c.find(class_='section-cols clearfix').find('ul').find_all('li')
    for i in c1[1:]:
        tel=i.find(class_="tel").text
        a=i.find('a')['href']
        num=a[-10:-4]
        dictTel.update({tel:num})
    global workerid,data2,b
    if telephone in dictTel:        
        workerid=dictTel[telephone]
        print('           刷新成功')
        data2['workerid']=workerid
        b+=1
    else:
        print('    未在第一页找到信息\n    正在检测是否被下架')
        start()
    
def job():  #请求程序
    r=requests.session()
    print('           登录中...')
    c=r.post(url1,headers=headers,data=data1)
    print(' ',c,'登录成功',)
    time.sleep(round(random.uniform(0,1),1))
    print('           刷新中...')
    res=r.post(url,headers=headers,data=data2)
    print(' ',res,'提交成功')
    time.sleep(random.randint(1,2))
    find1()
    global b,bb
    print(f'  已刷新 {b} 次,累计被下架{bb}次')
    tm=random.randint(1800,2400)  #刷新间隔时间
    for i in range (tm,0,-1):
        print(f'   距离下次刷新还有 {i} 秒',end='\r')
        time.sleep(1)
start()
time.sleep(random.randint(5,10))
os.system("cls")
content=False
while True:
    if content==True:
        data2['content']='女童针织t恤和裙子都做,不是加工厂,已经开工,急招员工,工价高,详谈加我微信或者打给我电话'
        content=False
    else:
        data2['content']='女童针织T恤和裙子都做,不是加工厂,已经开工,急招员工,工价高,详谈加我微信或者打给我电话'
        content=True
    job()
    os.system("cls")
   
