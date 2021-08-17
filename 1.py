import pandas as pd
import requests
import execjs
import time
import datetime
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
}
match_info=[]
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
get_match_info()
match_info_df=pd.DataFrame(match_info,columns=['场次ID','联赛','主队','客队','开始时间'])
def get_pan_info(match_id):
    match={}
    op_url='http://1x2d.win007.com/'+ str(match_info[0][0])+'.js'
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
    match['欧主初赔']=avg_org_op[0]
    match['欧初平赔']=avg_org_op[1]
    match['欧客初赔']=avg_org_op[2]
    match['欧主临赔']=avg_last_op[0]
    match['欧平临赔']=avg_last_op[1]
    match['欧客临赔']=avg_last_op[2]
    #time.sleep(3)
    yp_url='http://www.310win.com/handicap/'+str(match_info[0][0])+'.html'
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
    ball_url='http://www.310win.com/overunder/'+str(match_info[0][0])+'.html'
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
    return match
pan_info=[]
for i in match_info[:10]:
    pan_info.append(get_pan_info(i[0]))
match_info_df=pd.merge(match_info_df,pd.DataFrame)
match_info_df.to_excel('今日球赛.xlsx')