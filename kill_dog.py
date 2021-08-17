import pandas as pd
import requests
import re
import datetime
import time
import pymysql
import execjs
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] Kill Dog 启动中......')
reg = re.compile(r'<tr class="matchTr" matchid="(.*?)">')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
}
mp1={'nan':None,'半球': 0.5, '平手': 0, '半/一': 0.75, '平/半': 0.25, '一球': 1, '一/球半': 1.25, '球半': 1.5, '两球': 2, '球半/两': 1.75, '两球/两球半':2.25, '两球半/三球':2.75,
    '三球/三球半':3.25,'两球半/三球':2.75,'两半': 2.5, '两半/三': 2.75, '三球': 3, '两/两半': 2.25, '三/三半': 3.25, '三半': 3.5, '三球半':3.5,'三球半/四球':3.75,'两球半':2.5,'四球/四球半':4.25,
    '四球半/五球':4.75,'四球半':4.5,'五球':5,'半球': 0.5, '平手': 0, '半/一': 0.75, '平/半': 0.25, '一球': 1, '一/球半': 1.25, '球半': 1.5, '两球': 2, '球半/两': 1.75,
    '两球/两球半':2.25, '两球半/三球':2.75,
    '三球/三球半':3.25,'两球半/三球':2.75,'两半': 2.5, '两半/三': 2.75, '三球': 3, '两/两半': 2.25, '三/三半': 3.25, '三半': 3.5, '三球半':3.5,'三球半/四球':3.75,
    '三半/四': 3.75, '四球': 4, '四/四半': 4.25, '四半': 4.5, '四半/五': 4.75, '五球': 5, '半球/一球': 0.75, '一球/球半': 1.25, '球半/两球': 1.75,  '平手/半球': 0.25,
    '五球半/六球':5.75,'五球半':5.5,'六球':6,'五球/五球半':5.25,
    '三半/四': 3.75, '四球': 4, '四/四半': 4.25, '四半': 4.5, '四半/五': 4.75, '五球': 5, '半球/一球': 0.75, '一球/球半': 1.25, '球半/两球': 1.75,  '平手/半球': 0.25}
mp2={'nan':None,'2.5/3球':2.75, '2.5球':2.5, '3球':3, '3.5球':3.5, '3/3.5球':3.25, '2/2.5球':2.25,'2球':2, '1.5/2球':1.75, '1.5球':1.5,
        '3.5/4球':3.75, '4球':4,'3.5球':3.5,'4/4.5球':4.25,'4.5球':4.5,'4.5/5球':4.75,'5.0球':5,'4.75球':4.75,'2.5/3':2.75, '2.5':2.5, '3':3, '3.5':3.5, '3/3.5':3.25, '2/2.5':2.25,'2':2, '1.5/2':1.75, '1.5':1.5,
        '3.5/4':3.75, '4':4,'3.5':3.5,'4/4.5':4.25,'4.5':4.5,'4.5/5':4.75,'5.0':5,'4.75':4.75,'5.5':5.5,'5/5.5':5.25,'5.5/6':5.75,'6':6,'5':5,'nan':None,'2.5/3球':2.75, '2.5球':2.5, '3球':3, '3.5球':3.5, '3/3.5球':3.25, '2/2.5球':2.25,'2球':2, '1.5/2球':1.75, '1.5球':1.5,
        '3.5/4球':3.75, '4球':4,'3.5球':3.5,'4/4.5球':4.25,'4.5球':4.5,'4.5/5球':4.75,'5.0球':5,'4.75球':4.75,'2.5/3':2.75, '2.5':2.5, '3':3, '3.5':3.5, '3/3.5':3.25, '2/2.5':2.25,'2':2, '1.5/2':1.75, '1.5':1.5,
        '3.5/4':3.75, '4':4,'3.5':3.5,'4/4.5':4.25,'4.5':4.5,'4.5/5':4.75,'5.0':5,'4.75':4.75,'5.5':5.5,'5/5.5':5.25,'5.5/6':5.75,'6':6,'5':5,'6.5/7':6.75,'6.5':6.5,'6/6.5':6.25,'7.0':7}

title=["欧主初赔","欧初平赔","欧客初赔","欧主临赔","欧平临赔","欧客临赔","初盘","临盘","主初赔","客初赔","主临赔","客临盘赔","球初盘","球临盘","大球初盘","小球初盘","大球临盘","小球临盘"]
def create_cmd(params):
    try:
        if len(params)==12:
            cmd="""SELECT 	
	        `football_sheet3.0`.`赛果` 
                    FROM`football_sheet3.0` ORDER BY(
            ABS( %f- `football_sheet3.0`.`欧主初赔` )+ 
            abs( %f- `football_sheet3.0`.`欧初平赔` )+ 
            abs( %f- `football_sheet3.0`.`欧客初赔` )+ 
            abs( %f- `football_sheet3.0`.`欧主临赔` )+ 
            abs( %f- `football_sheet3.0`.`欧平临赔` )+ 
            abs( %f- `football_sheet3.0`.`欧客临赔` )+ 
            abs( %f- `football_sheet3.0`.`初盘` )+ 
            abs( %f- `football_sheet3.0`.`临盘` )+ 
            abs( %f- `football_sheet3.0`.`主初赔` )+ 
            abs( %f- `football_sheet3.0`.`客初赔` )+ 
            abs( %f- `football_sheet3.0`.`主临赔` )+ 
            abs(%f- `football_sheet3.0`.`客临盘赔`))"""%(tuple(params))
        else:
            cmd="""SELECT
		`football_sheet3.0`.`总进球`,
        `football_sheet3.0`.`球临盘`
                    FROM
                        `football_sheet3.0`
                    ORDER BY(
        abs(%f -`football_sheet3.0`.`球初盘`)+ 
        abs(%f -`football_sheet3.0`.`球临盘`)+ 
        abs(%f -`football_sheet3.0`.`大球初盘`)+ 
        abs(%f -`football_sheet3.0`.`小球初盘`)+ 
        abs(%f -`football_sheet3.0`.`大球临盘`)+ 
        abs(%f -`football_sheet3.0`.`小球临盘`))"""%(tuple(params))
        return cmd
    except :
        print('参数有误,请重试')
        return False
match_info=[]
pan_info=[]
single_match_info=[]
def get_match_info():
    total_match_url='http://www.310win.com/info/match/data/bfdata.js'
    total_match=requests.get(total_match_url,headers=headers)
    js_data=execjs.compile(total_match.text.replace('ShowBf();',''))
    match_list=js_data.eval('A')
    match_info_idx=[0,2,5,8,11]
    for m in match_list:
        if not m: continue
        info=[]
        for i in match_info_idx:
            info.append(m[i].replace('<font color=#880000>(中)</font>',''))
        match_info.append(info)

def get_pan_info(match_id):
    match={}
    try:
        op_url='http://1x2d.win007.com/'+ str(match_id)+'.js'
        op_data=requests.get(op_url,headers=headers)
        op_data_js=execjs.compile(op_data.text)
        last_op=op_data_js.eval('gameDetail')
        org_op=op_data_js.eval('game')
        avg_org_op=[0,0,0]
        for i in range(len(org_op)):
            org_op[i] = org_op[i].split('|')
            avg_org_op[0]+=float(org_op[i][3])
            avg_org_op[1]+=float(org_op[i][4])
            avg_org_op[2]+=float(org_op[i][5])
        if len(org_op):
            avg_org_op=[avg_org_op[0]/len(org_op),avg_org_op[1]/len(org_op),avg_org_op[2]/len(org_op)]
        avg_last_op=[0,0,0]
        for i in range(len(last_op)):
            last_op[i] = last_op[i].split('|')
            avg_last_op[0]+=float(last_op[i][0][last_op[i][0].index('^')+1:])
            avg_last_op[1]+=float(last_op[i][1])
            avg_last_op[2]+=float(last_op[i][2])
        if len(last_op):
            avg_last_op=[avg_last_op[0]/len(last_op),avg_last_op[1]/len(last_op),avg_last_op[2]/len(last_op)]
        match['欧主初赔']=avg_org_op[0]
        match['欧初平赔']=avg_org_op[1]
        match['欧客初赔']=avg_org_op[2]
        match['欧主临赔']=avg_last_op[0]
        match['欧平临赔']=avg_last_op[1]
        match['欧客临赔']=avg_last_op[2]
        #time.sleep(3)
        yp_url='http://www.310win.com/handicap/'+str(match_id)+'.html'
        yp_data=requests.get(yp_url,headers=headers)
        #time.sleep(3)
        yp_tb=pd.read_html(yp_data.text)
        yp_tb=yp_tb[1]
        yp_tb.drop(index=[0,1])
        del yp_tb[list(yp_tb.columns)[8]]
        del yp_tb[list(yp_tb.columns)[7]]
        dp=[]
        for i in range(yp_tb.shape[0]):
            if not '金宝博' in yp_tb.iloc[i][0]:dp.append(i)
        yp_tb=yp_tb.drop(index=dp)
        yp_tb=yp_tb.iloc[0].tolist()[1:]
        match['初盘']=yp_tb[1]
        match['临盘']=yp_tb[4]
        match['主初赔']=yp_tb[0]
        match['客初赔']=yp_tb[2]
        match['主临赔']=yp_tb[3]
        match['客临盘赔']=yp_tb[5]
        ball_url='http://www.310win.com/overunder/'+str(match_id)+'.html'
        ball_data=requests.get(ball_url,headers=headers)
        ball_tb=pd.read_html(ball_data.text)[1]
        ball_tb.drop(index=[0,1])
        del ball_tb[list(ball_tb.columns)[8]]
        del ball_tb[list(ball_tb.columns)[7]]
        dp=[]
        for i in range(ball_tb.shape[0]):
            if not '金宝博' in ball_tb.iloc[i][0]:dp.append(i)
        ball_tb=ball_tb.drop(index=dp)
        ball_tb=ball_tb.iloc[0].tolist()[1:]
        match['球初盘']=ball_tb[1]
        match['球临盘']=ball_tb[4]
        match['大球初盘']=ball_tb[0]
        match['小球初盘']=ball_tb[2]
        match['大球临盘']=ball_tb[3]
        match['小球临盘']=ball_tb[5]
    except:
        match['初盘']='获取失败'
        match['临盘']='获取失败'
        match['主初赔']='获取失败'
        match['客初赔']='获取失败'
        match['主临赔']='获取失败'
        match['客临盘赔']='获取失败'
        match['欧主初赔']='获取失败'
        match['欧初平赔']='获取失败'
        match['欧客初赔']='获取失败'
        match['欧主临赔']='获取失败'
        match['欧平临赔']='获取失败'
        match['欧客临赔']='获取失败'
        match['球初盘']='获取失败'
        match['球临盘']='获取失败'
        match['大球初盘']='获取失败'
        match['小球初盘']='获取失败'
        match['大球临盘']='获取失败'
        match['小球临盘']='获取失败'
    return match

def get_allpan_info(match_id=None):
    if not match_id:
        global pan_info
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 获取盘口信息中,大约需要1分钟')
        for i in match_info:
            pan_info.append(get_pan_info(i[0]))
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 即将对所有比赛进行预测，请耐心等待，大约需要3分钟')
        analyze_all(pan_info)
    else:
        analyze_single_match([get_pan_info(match_id=match_id)])

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 获取今天的比赛中,大约需要1分钟')
get_match_info()
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 获取比赛成功！共',len(match_info),'场比赛')
match_info_df=pd.DataFrame(match_info,columns=['场次ID','联赛','主队','客队','开始时间'])
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 数据初始化完成,即将为你生成Excle表格')
match_info_df.to_excel('今日球赛'+datetime.datetime.now().strftime("%Y-%m-%d")+'.xlsx')
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 表格生成成功！请打开当前文件夹查看')

class Analyzer():
    def __init__(self):
        self.sheet = pymysql.connect(host='your database host', port=3306,
                                     user='your database user', passwd='your database password', db='database name')
        self.all_match=[]
        self.cursor = self.sheet.cursor()
        self.res = ()
        self.cmd=''
    def analyze(self, cmd,is_ball):
        self.cursor.execute(cmd)
        res=self.cursor.fetchall()[:10]
        title=['主胜','客胜','平局']
        if not is_ball: 
            analyzed_data=[0,0,0]
            for i in res:
                analyzed_data[i[0]]+=1
            if analyzed_data.count(max(analyzed_data))!=1:
                return '非'+title[analyzed_data.index(min(analyzed_data))]
            else:return title[analyzed_data.index(max(analyzed_data))]
        else:
            is_big_ball=0
            for i in res:
                if i[0]>i[1]:is_big_ball+=1
            if is_big_ball>5:
                return '大'
            else:
                return '小'
    def close(self):
        self.sheet.commit()
        self.cursor.close()
        self.sheet.close()
myAnalyzer=Analyzer()
def analyze_all(pan_info):
    global match_info_df
    for m in range(len(pan_info)):
        params=[]
        zeros=0
        if '获取失败' in pan_info[m].values():
            continue
        if str(pan_info[m]['临盘'])==str(float('nan')) or str(pan_info[m]['初盘'])==str(float('nan')) or str(pan_info[m]['球临盘'])==str(float('nan')) or str(pan_info[m]['球初盘'])==str(float('nan')):
            continue
        if '受' in str(pan_info[m]['临盘']) :
            pan_info[m]['临盘']=-mp1[pan_info[m]['临盘'][1:]]
        else:pan_info[m]['临盘']=mp1[pan_info[m]['临盘']]
        if '受' in str(pan_info[m]['初盘']) :
            pan_info[m]['初盘']=-mp1[pan_info[m]['初盘'][1:]]
        else:pan_info[m]['初盘']=mp1[pan_info[m]['初盘']]
        pan_info[m]['球临盘'] =mp2[pan_info[m]['球临盘']]
        pan_info[m]['球初盘'] =mp2[pan_info[m]['球初盘']]
        if '无法获取' in pan_info[m]:
            continue
        for info in title:
            if pan_info[m][info]==0:
                zeros+=1
            if str(pan_info[m][info])==str(float('nan')): 
                zeros=4
                break
            params.append(float(pan_info[m][info]))
        if zeros>=3:
            continue
        try:
            ball_cmd=create_cmd(params[12:])
            win_cmd=create_cmd(params[:12])
            pan_info[m]['胜负预测']=myAnalyzer.analyze(win_cmd,0)
            pan_info[m]['大球预测']=myAnalyzer.analyze(ball_cmd,1)
        except :print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 第',m,'场分析失败,可能是没开盘')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 分析完成,即将为你生成Excle表格')
    match_info_df=pd.concat([match_info_df,pd.DataFrame(pan_info)],axis=1)
    match_info_df.to_excel('今日球赛--含预测'+datetime.datetime.now().strftime("%Y-%m-%d")+'.xlsx')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 表格生成成功！请打开当前文件夹查看')
    return

def analyze_single_match(pan_info):
    try:
        m=0
        params=[]
        zeros=0
        if '受' in str(pan_info[m]['临盘']) :
            pan_info[m]['临盘']=-mp1[pan_info[m]['临盘'][1:]]
        else:pan_info[m]['临盘']=mp1[pan_info[m]['临盘']]
        if '受' in str(pan_info[m]['初盘']) :
            pan_info[m]['初盘']=-mp1[pan_info[m]['初盘'][1:]]
        else:pan_info[m]['初盘']=mp1[pan_info[m]['初盘']]
        pan_info[m]['球临盘'] =mp2[pan_info[m]['球临盘']]
        pan_info[m]['球初盘'] =mp2[pan_info[m]['球初盘']]
        for info in title:
            if pan_info[m][info]==0:
                zeros+=1
            if str(pan_info[m][info])==str(float('nan')): 
                zeros=4
                break
            params.append(float(pan_info[m][info]))
        if zeros>=3:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 分析失败,可能是没开盘')
        try:
            ball_cmd=create_cmd(params[12:])
            win_cmd=create_cmd(params[:12])
            pan_info[m]['胜负预测']=myAnalyzer.analyze(win_cmd,0)
            pan_info[m]['大球预测']=myAnalyzer.analyze(ball_cmd,1)
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 分析成功')
            print(pan_info[m])
            return
        except :
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 分析失败,可能是没开盘')
            return
    except:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] ',m,'分析失败,可能是没开盘')
def show_menu():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 菜单初始化中。')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 菜单初始化完成。')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 功能选项：')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 1.分析单场比赛')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 2.分析今日全部比赛')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 3.退出程序')
def execute_operation(operation):
    if operation==1:
        match_id=input(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' [*] 输入你要分析的比赛的ID，可以查看比赛Excle文件第一列\n')
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 分析'+match_id+'中')
        get_allpan_info(match_id)
    if operation==2:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'[*] 分析全部比赛需要2-3分钟，并且可能导致IP被封，无法继续使用，请确定是否继续')
        cf=input(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' [*] 你确定吗？输入N/n取消\n')
        if cf=='n' or cf=='N': return 
        global pan_info
        get_allpan_info()
        analyze_all(pan_info)
    if operation==3:
        exit(0)
while 1:
    show_menu()
    option=input(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' [*] 输入你要执行的操作\n')
    option=int(option)
    execute_operation(option)
