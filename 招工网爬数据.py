import requests,json,re,time,random,os,datetime,openpyxl
from bs4 import BeautifulSoup

zhaogong=r'C:\Users\Administrator\Desktop\招工.xlsx'
gengxin=r'C:\Users\Administrator\Desktop\招工更新信息.xlsx'
# 以下为排序模块
def paixu(x):    
    import re,collections
    wb = openpyxl.load_workbook(x)
    sheet = wb['求职列表']
    c=sheet['i']
    row=0
    timedict={}
    for i in c:
        row=row+1
        if row==1:
            continue
        timedict.update({row:int(re.sub(r'\D', "", i.value))})
    d=collections.Counter(timedict).most_common()#按照表格的值把字典转换成元组排序
    listcache=[]
    listcache.append(None)
    for i in range(1,sheet.max_row+1):
        rowcache=[]
        for ii in sheet[i]:
            rowcache.append(ii.value)
        listcache.append(rowcache)

    wb1=openpyxl.Workbook()
    sheet1 = wb1.active
    sheet1.title ='求职列表'
    sheet1.append(listcache[1])
    for i in d:
        sheet1.append(listcache[i[0]])
    wb1.save(x)
    

#以下为清理重复数据模块
def clean(x):    
    wb = openpyxl.load_workbook(x)
    sheet = wb['求职列表']
    c=sheet.iter_cols(min_col=4,max_col=4,values_only=True)
    dict1={}
    dict2={}
    list1=[]
    num=1
    for ii in c:
        for i in ii:
            dict1.update({num:i})
            num=num+1

    for i in dict1:
        if dict1[i] in dict2:
            list1.append(i)
            continue
        c={dict1[i]:i}
        dict2.update(c)

    for i in reversed(list1):
        sheet.delete_rows(i)
    wb.save(x)

list1=[]#爬取信息暂存
r=requests.session()#建立会话
with open('招工cookies.txt','r',encoding='utf-8') as f:
    cookies=f.read()
d_dict=json.loads(cookies)
e=requests.utils.cookiejar_from_dict(d_dict)
r.cookies=e
have=False

if os.path.isfile(zhaogong)==True:#查询是否有'招工.xlsx'文件,如果有就读取最近一条数据的时间,爬取时间有之前的就终止爬取
    have=True
    wb= openpyxl.load_workbook(zhaogong)
    sheet = wb['求职列表']
    c=sheet['i2'].value   
    d=int(re.sub(r'\D',"",c))
    have1=d
namelist=['车工','机工','缝纫']
for name in namelist:
    T=True #爬取开关
    for page in range(1,100):
        url_1 = f'https://www.zlrcsc.com/mobile/worker/index/key/{name}/page/{page}.htm'
        res = r.get(url_1)
        c=BeautifulSoup(res.text, 'html.parser')
        c1=c.find(class_='section-cols clearfix').find('ul').find_all('li')
        num=0
        for i in c1:
            if num==0:
                num=num+1
                continue  
            url_next='https://www.zlrcsc.com'+ i.find('a')['href']
            num=num+1
            resi=r.get(url_next)
            ci=BeautifulSoup(resi.text,'html.parser')
            cii=ci.find_all(class_="list_height plist-txt notarrow")
            listcache=[]
            for ii in cii:
                input1=ii.find('div',class_="describe").text.strip()
                if len(input1)==11 and input1.isdigit():
                    input1=input1[0:3]+' '+input1[3:7]+' '+input1[7:11]
                listcache.append(input1)
            bc=ci.find(class_="com-introduce").text.strip()
            listcache.append(bc)
            tm=ci.find(class_="titlebot_title").text
            mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",tm).group()
            listcache.append(mat)
            nowtime=datetime.datetime.now().strftime("%Y-%m-%d")
            nowtime1=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            if have==False:
                if nowtime not in mat and nowtime1 not in mat:
                    T=False
                    break
            else:
                if int(re.sub(r'\D',"",mat)) <= have1:
                    T=False
                    break
            print(listcache)
            list1.append(tuple(listcache))
            time.sleep(round(random.uniform(0.2,0.8),1))
        if T==False:
            break

T1=False 
if os.path.isfile(zhaogong)==True:
    wb = openpyxl.load_workbook(zhaogong)
    sheet = wb['求职列表']
    T1=True
else:
    wb = openpyxl.Workbook() 
    sheet = wb.active
    sheet.title ='求职列表'
    sheet.append(['名称','工资','称呼','联系方式','年龄','性别','家乡','备注','发布时间'])
for i in list1:
    sheet.append(i)  
wb.save(zhaogong)
paixu(zhaogong)
clean(zhaogong)
if T1:
    wb = openpyxl.Workbook() 
    sheet = wb.active
    sheet.title ='求职列表'
    sheet.append(['名称','工资','称呼','联系方式','年龄','性别','家乡','备注','发布时间'])
    for i in list1:
        sheet.append(i)  
    wb.save(gengxin)
    paixu(gengxin)
    clean(gengxin)

print('保存成功')