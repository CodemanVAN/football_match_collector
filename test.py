import pandas as pd
import requests
import re
import datetime
import time
import pymysql
reg = re.compile(r'<tr class="matchTr" matchid="(.*?)">')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
}
mp1 = {
    '半球': 0.5, '平手': 0, '半/一': 0.75, '平/半': 0.25, '一球': 1, '一/球半': 1.25,  '球半': 1.5, '两球': 2, '球半/两': 1.75, '两半': 2.5, '两半/三': 2.75,
    '三球': 3, '两/两半': 2.25, '三/三半': 3.25, '三半': 3.5, '三半/四': 3.75, '四球': 4, '四/四半': 4.25, '四半': 4.5, '四半/五': 4.75, '五球': 5
}
mp2 = {'2.5/3球': 2.75, '2.5球': 2.5, '3球': 3, '3.5球': 3.5, '3/3.5球': 3.25, '2/2.5球': 2.25, '2球': 2, '1.5/2球': 1.75, '1.5球': 1.5,
       '3.5/4球': 3.75, '4球': 4, '3.5球': 3.5, '4/4.5球': 4.25, '4.5球': 4.5, '4.5/5球': 4.75, '5.0球': 5, '4.75球': 4.75}
win_cmd="""SELECT
	`football_sheet2.0`.`欧主初赔`,
	`football_sheet2.0`.`欧初平赔`,
	`football_sheet2.0`.`欧客初赔`,
	`football_sheet2.0`.`欧主临赔`,
	`football_sheet2.0`.`欧平临赔`,
	`football_sheet2.0`.`欧客临赔`,
	`football_sheet2.0`.`初盘`,
	`football_sheet2.0`.`临盘`,
	`football_sheet2.0`.`主初赔`,
	`football_sheet2.0`.`客初赔`,
	`football_sheet2.0`.`主临赔`,
	`football_sheet2.0`.`客临盘赔` FROM`football_sheet2.0` ORDER BY
 (ABS( %f- `football_sheet2.0`.`欧主初赔` )+ abs( %f- `football_sheet2.0`.`欧初平赔` )+ abs( %f- `football_sheet2.0`.`欧客初赔` )+ abs( %f- `football_sheet2.0`.`欧主临赔` )+ abs( %f- `football_sheet2.0`.`欧平临赔` )+ abs( %f- `football_sheet2.0`.`欧客临赔` )+ abs( %f- `football_sheet2.0`.`初盘` )+ abs( %f- `football_sheet2.0`.`临盘` )+ abs( %f- `football_sheet2.0`.`主初赔` )+ abs( %f- `football_sheet2.0`.`客初赔` )+ abs( %f- `football_sheet2.0`.`主临赔` )+ abs(%f- `football_sheet2.0`.`客临盘赔`))"""

class Analyzer():
    def __init__(self):
        self.sheet = pymysql.connect(host='1.116.145.211', port=3306,
                                     user='whatcoldwind', passwd='whatcoldwind', db='football')
        # 创建游标
        self.all_match=[]
        self.cursor = self.sheet.cursor()
        self.res = ()
        self.cmd=''
    def analyze(self, cmd=None,limit=20):
        if not cmd:
            self.cursor.execute(self.cmd)
        else:
            self.cursor.execute(cmd)
        self.res = list(self.cursor.fetchall())[:20]
        posibilities =[0,0,0]
        is_big_ball=[0,0]
        for m in range(10):
            posibilities[self.res[m][5]]+=1
            is_big_ball[self.res[m][-10]]+=1
        print('高置信度*平局，主胜，客胜 的概率为：',posibilities)
        print('高置信度*大球局可能性为（必收米）:',is_big_ball[1])
        posibilities =[0,0,0]
        is_big_ball=[0,0]
        for m in range(limit):
            posibilities[self.res[m][5]]+=1
            is_big_ball[self.res[m][-10]]+=1
        print('供参考*平局，主胜，客胜 的概率为 %：',posibilities[0]*10,posibilities[1]*10,posibilities[2]*10)
        print('供参考*大球局可能性为（必收米）%:',is_big_ball[1]*100/limit)
    def close(self):
        self.sheet.commit()
        self.cursor.close()
        self.sheet.close()

    def get_match_info(self, i):
        try:
            match_data = [None for j in range(28)]
            url2 = 'https://fenxi.zgzcw.com/'+str(i)+'/ypdb'
            rsp2 = requests.get(url2, headers=headers)
            tbs2 = pd.read_html(rsp2.text)
            yp = tbs2[2]
            yp = yp.iloc[[7]]
            match_data[5] = yp[2].values.tolist()[0]
            match_data[6] = yp[4].values.tolist()[0]
            match_data[7] = yp[3].values.tolist()[0]
            match_data[8] = yp[5].values.tolist()[0]
            match_data[9] = yp[7].values.tolist()[0]
            match_data[10] = yp[6].values.tolist()[0]
            match_data[11] = yp[9].values.tolist()[0]
            match_data[12] = yp[10].values.tolist()[0]
            time.sleep(5)
            url4 = 'https://fenxi.zgzcw.com/'+str(i)+'/dxdb'
            rsp4 = requests.get(url4, headers=headers)
            tbs4 = pd.read_html(rsp4.text)
            qiu = tbs4[2].iloc[[8]]
            match_data[13] = qiu[2].values.tolist()[0]
            match_data[14] = qiu[4].values.tolist()[0]
            match_data[15] = qiu[3].values.tolist()[0]
            match_data[16] = qiu[5].values.tolist()[0]
            match_data[17] = qiu[7].values.tolist()[0]
            match_data[18] = qiu[6].values.tolist()[0]
            time.sleep(5)
            url3 = 'https://fenxi.zgzcw.com/'+str(i)+'/bjop'
            rsp3 = requests.get(url3, headers=headers)
            tbs3 = pd.read_html(rsp3.text)
            op = tbs3[-1].iloc[[0]]
            match_data[19] = op[2].values.tolist()[0]
            match_data[20] = op[4].values.tolist()[0]
            match_data[21] = op[3].values.tolist()[0]
            match_data[22] = op[5].values.tolist()[0]
            match_data[23] = op[7].values.tolist()[0]
            match_data[24] = op[6].values.tolist()[0]
            match_data[25] = op[9].values.tolist()[0]
            match_data[26] = op[11].values.tolist()[0]
            match_data[27] = op[10].values.tolist()[0]
            for info in range(5, len(match_data)):
                if '↑' in str(match_data[info]) or '↓' in str(match_data[info]):
                    match_data[info] = match_data[info].replace('↓', '')
                    match_data[info] = match_data[info].replace('↑', '')
                if match_data[info] in mp1.keys():
                    match_data[info] = mp1[match_data[info]]
                if match_data[info] in mp2.keys():
                    match_data[info] = mp2[match_data[info]]
                if '受' in str(match_data[info]):
                    match_data[info] = -mp1[match_data[info][1:]]
                match_data[info] = float(match_data[info])
            match_data.append(match_data[18]-match_data[15])
            match_data.append(match_data[16]-match_data[13])
            match_data.append(match_data[17]-match_data[14])
            match_data.append(match_data[10]-match_data[7])
            match_data.append(match_data[8]-match_data[5])
            match_data.append(match_data[9]-match_data[6])
            match_data.append(match_data[22]-match_data[19])
            match_data.append(match_data[23]-match_data[20])
            match_data.append(match_data[24]-match_data[21])
            self.cmd = """SELECT * FROM `football_sheet` ORDER BY (ABS(%f - `主初赔`) + ABS(%f - `客初赔`) + ABS(%f - `初盘`) + ABS(%f - `主临赔`) + ABS(%f - `客临盘赔`) + ABS(%f - `临盘`) + ABS(%f - `主胜概率`) + ABS(%f - `客胜概率`) + ABS(%f - `大球初盘`) + ABS(%f - `小球初盘`) + ABS(%f - `球初盘`) + ABS(%f - `大球临盘`) + ABS(%f - `小球临盘`) + ABS(%f - `球临盘`) + ABS(%f - `欧主初赔`) + ABS(%f - `欧客初赔`) + ABS(%f - `欧初平赔`) + ABS(%f - `欧主临赔`) + ABS(%f - `欧客临赔`) + ABS(%f - `欧平临赔`) + ABS(%f - `欧主概率`) + ABS(%f - `欧平概率`) + ABS(%f - `欧客概率`) + ABS(%f - `大球盘变化`) + ABS(%f - `大球赔变化`) + ABS(%f - `小球赔变化`) + ABS(%f - `让盘变化`) + ABS(%f - `亚主赔变化`) + ABS(%f - `亚客赔变化`) + ABS(%f - `欧主赔变化`) + ABS(%f - `欧客赔变化`) + ABS(%f - `欧平赔变化`))
                    """%(tuple(match_data[5:]))
            self.analyze()
        except :print('获取信息失败，可能你被封IP了，等等再试试.')
    def analyze_all_match(self):
        for i in self.all_match:
            self.get_match_info(i)
myAnalyzer=Analyzer()
def get_match_table_info():
    global myAnalyzer
    try:
        url = 'https://live.zgzcw.com/qb/'
        rsp = requests.get(url=url, headers=headers)
        data = pd.read_html(rsp.text)
        match_ID = re.findall(reg, rsp.text)
        now_match = data[0]
        title = ['序号', '赛事', '轮次', '时间', '状态', '主队', '比分', '客队', '半场', '欧赔亚盘', '直播',
                 '分析', '走地']
        need_title = ['时间', '状态', '主队', '比分', '客队', '半场']
        for i in title:
            if not i in need_title:
                del now_match[i]
        now_match = now_match.drop(index=[0])
        now_match = now_match.drop(
            now_match[now_match['状态'] == '最新赛果'].index.tolist()[0])
        end_match = now_match[now_match['状态'].isin(['完'])]
        upcoming_match = now_match[now_match['状态'].isin(['未'])]
        started_match = now_match[(~now_match['状态'].isin(['完']))
                                  & (~now_match['状态'].isin(['未']))]
        upcoming_match_ID = match_ID[:upcoming_match.shape[0]]
        upcoming_match['场次ID'] = upcoming_match_ID
        started_match['场次ID'] = match_ID[upcoming_match.shape[0]:upcoming_match.shape[0]+started_match.shape[0]]
        end_match['场次ID'] = match_ID[-end_match.shape[0]:]
        upcoming_match.to_excel('即将开始的比赛.xlsx')
        end_match.to_excel('已经结束的比赛.xlsx')
        started_match.to_excel('正在进行中的比赛.xlsx')
        myAnalyzer.all_match=upcoming_match_ID
        print('共', upcoming_match.shape[0], '即将开始')
        print('共', started_match.shape[0], '正在进行')
        print('共', end_match.shape[0], '已经结束')
    except:
        print('获取失败')

if __name__=='__main__':
    print('****************************************************************')
    print('****************欢迎使用Kill Dog 庄足球分析软件*****************')
    print('****************************************************************')
    while 1:
        print(
            """|*************************菜单**********************************|\n
    |** 1:获取当前比赛信息并生成Excel表格.                            \n 
    |** 2:输入场次ID进行自动分析.                                     \n
    |** 3:分析全部未开始的比赛
    |** 4:退出软件.                                                  \n
    """)
        op=input('输入你要的操作\n')
        if op=='1':
            print("开始获取",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            get_match_table_info()
            print("获取成功",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if op=='2':
            need_to_analayz_match_id=input("输入Excle表格中的场次ID\n")
            try:
                print('开始分析中，大约需要1分钟',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                myAnalyzer.get_match_info(need_to_analayz_match_id)
                print('分析完毕',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            except:print('出错了，请重试')
        if op=='3':
            print(myAnalyzer.all_match)
        if op=='4':
            print('退出中，欢迎下次使用，再见')
            
            time.sleep(1)
            exit(0)
