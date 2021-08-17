# coding:gbk
import requests
import execjs
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
}
headers={
'Referer':'http://info.310win.com/cn/League/2020-2021/36.html',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'}
import requests
import execjs
import pandas as pd
import datetime
import time
import os

leagues_url='http://info.310win.com/jsData/infoHeader.js'
leagues_data=requests.get(leagues_url,headers=headers)
if leagues_data.status_code==200:
    leagues_data_js=execjs.compile(str(leagues_data.text)[1:])
leagues_list=leagues_data_js.eval('arr')
target=[]
for i in leagues_list:
    data={}
    data['country_name']=i[1]
    for t in i[4]:
        t=t.split(',')
        data['id']=t[0]
        data['lg_name']=t[1]
        data['seasons']=t[5:5+4]
        break
    target.append(data)
start=None
end=None
while start==None or end==None:
    try:
        start=input('输入爬取的开始标号 1 -- 116\n')
        start=int(start)
    except :
        print('输入不对，请输入数字再回车 例如 10 然后回车')
        start=None
        end=None
        continue
    try:
        end=input('输入爬取的结束的标号 1 -- 116\n')
        end=int(end)
    except :
        print('输入不对，请输入数字再回车 例如 10 然后回车')
for tournament in target[start:end]:
    for year in tournament['seasons']:
        league_detail_url='http://info.310win.com/jsData/matchResult/'+year+'/s'+str(tournament['id'])+'.js'
        league_detail_data=requests.get(league_detail_url,headers=headers)
        have_download=os.listdir()
        if tournament['lg_name']+year+'数据.xlsx' in have_download:
            print(tournament['lg_name']+year+'数据.xlsx','下载过了，自动跳过')
            continue
        if league_detail_data.status_code!=200:
            print('err')
        else:
            try:
                print('爬取',tournament['country_name'],year,tournament['lg_name'],'中',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                league_detail_data_js=execjs.compile('var jh= {};'+league_detail_data.text[1:])
                league_detail_name=league_detail_data_js.eval('arrLeague')[2]
                league_detail_team_row=league_detail_data_js.eval('arrTeam')
                league_detail_team={}
                for i in league_detail_team_row:
                    league_detail_team[i[0]]=i[1]
                league_detail_match=league_detail_data_js.eval('jh')
                all_match=[]
                for r in sorted(list(league_detail_match.keys())):
                    for m in league_detail_match[r]:
                        match={}
                        match['id']=m[0]
                        match['time']=m[3]
                        match['host']=league_detail_team[m[4]]
                        match['guest']=league_detail_team[m[5]]
                        match['full_res']=m[6]
                        match['half_res']=m[7]
                        match['give_full']=m[10]
                        match['give_half']=m[11]
                        match['sc_full']=m[12]
                        match['sc_half']=m[13]
                        op_url='http://1x2d.win007.com/'+ str(match['id'])+'.js'
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
                        avg_org_op=[avg_org_op[0]/len(org_op),avg_org_op[1]/len(org_op),avg_org_op[2]/len(org_op)]
                        avg_last_op=[0,0,0]
                        for i in range(len(last_op)):
                            last_op[i] = last_op[i].split('|')
                            avg_last_op[0]+=float(last_op[i][0][last_op[i][0].index('^')+1:])
                            avg_last_op[1]+=float(last_op[i][1])
                            avg_last_op[2]+=float(last_op[i][2])
                        avg_last_op=[avg_last_op[0]/len(last_op),avg_last_op[1]/len(last_op),avg_last_op[2]/len(last_op)]
                        match['op_org_host']=avg_org_op[0]
                        match['op_org_equal']=avg_org_op[1]
                        match['op_org_guest']=avg_org_op[2]
                        match['op_last_host']=avg_last_op[0]
                        match['op_last_equal']=avg_last_op[1]
                        match['op_last_guest']=avg_last_op[2]
                        #time.sleep(3)
                        yp_url='http://www.310win.com/handicap/'+str(match['id'])+'.html'
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
                        match['yp_org_give_full']=yp_tb[1]
                        match['yp_last_give_half']=yp_tb[4]
                        match['yp_org_host']=yp_tb[0]
                        match['yp_org_guest']=yp_tb[2]
                        match['yp_last_host']=yp_tb[3]
                        match['yp_last_guest']=yp_tb[5]
                        #time.sleep(3)
                        ball_url='http://www.310win.com/overunder/'+str(match['id'])+'.html'
                        ball_data=requests.get(ball_url,headers=headers)
                        #time.sleep(3)
                        ball_tb=pd.read_html(ball_data.text)[1]
                        ball_tb.drop(index=[0,1])
                        del ball_tb[list(ball_tb.columns)[8]]
                        del ball_tb[list(ball_tb.columns)[7]]
                        dp=[]
                        for i in range(ball_tb.shape[0]):
                            if not '金宝博' in ball_tb.iloc[i][0]:dp.append(i)
                        ball_tb=ball_tb.drop(index=dp)
                        ball_tb=ball_tb.iloc[0].tolist()[1:]
                        match['org_ball']=ball_tb[1]
                        match['last_ball']=ball_tb[4]
                        match['org_big_ball']=ball_tb[0]
                        match['org_small_ball']=ball_tb[2]
                        match['last_big_ball']=ball_tb[3]
                        match['last_small_ball']=ball_tb[5]
                        all_match.append(match)
                    dt=pd.DataFrame(all_match)
                    dt.to_excel(tournament['lg_name']+year+'数据.xlsx')
            except:
                print(tournament['country_name']+tournament['lg_name']+year+'无法获取',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
