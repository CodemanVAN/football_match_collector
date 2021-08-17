import requests
import pandas as pd
import re
import time
import datetime
import os
reg = re.compile(r'http://fenxi.zgzcw.com/(.*?)/ypdb')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
}
baseparams = {'source_league_id': 36,
              'currentRound': 1,
              'season': '2020-2021'}
'''{'爱超': [1, '36'], '阿甲': [2, '25'], '奥甲': [3, '22'], '巴甲': [4, '38'], '比甲': [5, '34'], '波兰超': [6, '34'], '丹麦超': [7, '22'], '德甲': [8, '34'], 
'德乙': [9, '34'], '俄超': [10, '30'], '法甲': [11, '38'], '法乙': [12, '38'], '芬超': [13, '22'], '韩K联': [15, '33'], '荷甲': [16, '34'], '荷乙': [17, '38'], '美职': [21, '34'], '挪超': [22, '30'], '葡超': [23, '34'], '日职': [25, '38'], '瑞典超': [26, '30'], '瑞士超': [27, '36'], '苏超': [29, '33'], '土超': [30, '38'], '西甲': [31, '38'], '希腊超': [32, '26'], '西乙': [33, '42'], '意甲': [34, '38'], '英乙': [35, '46'], '英超': [36, '38'], '英冠': [37, '46'], '英甲': [39, '46'], '意乙': [40, '38'], '中超': [60, '14'], '中甲': [61, '10'], '以超': [118, '26'], '乌克超': [119, '30'], '斯亚乙': [120, '30'], '瑞士甲': [121, '36'], '瑞典甲': [122, '30'], '挪甲': [123, '30'], '罗甲': [124, '30'], '丹麦甲': [127, '22'], '奥乙': [128, '30'], '塞尔超': [129, '30'], '土甲': [130, '38'], '保超': [131, '12'], '斯伐超': [132, '22'], '克亚甲': [133, '36'], '威超': [135, '22'], '匈甲': [136, '33'], '捷甲': [137, '29'], '比乙': [138, '28'], '爱甲': [139, '27'], '墨超': [140, '17'], '意丙1A': [142, '37'], '英议联': [146, '45'], '苏冠': [150, '36'], '苏甲': [151, '34'], '苏乙': [152, '34'], '葡甲': [157, '30'], '塞浦甲': [159, '14'], '以甲': [160, '17'], '北爱超': [165, '20'], '冰岛超': [166, '22'], '希腊甲': [170, '22'], '圣保罗锦': [178, '11'], '里约锦标': [181, '11'], '阿尔甲': [193, '38'], '新加坡联': [194, '21'], '英后南': [201, '17'], '法丙': [203, '33'], '芬甲': [212, '22'], '拉脱超': [214, '36'], '立陶甲': [
    217, '36'], '瑞典乙': [218, '30'], '波兰甲': [221, '32'], '白俄超': [230, '30'], '芬乙A': [233, '25'], '俄甲': [235, '36'], '乌拉甲': [240, '15'], '秘鲁甲': [242, '17'], '斯亚甲': [247, '34'], '哥伦甲': [250, '20'], '澳超': [273, '5'], '英后北': [274, '17'], '伊朗超': [279, '29'], '希腊丙': [281, '2'], '日乙': [284, '42'], '英女超': [285, '11'], '捷乙': [290, '27'], '沙特联': [292, '14'], '英议北': [297, '42'], '英议南': [298, '42'], '阿联酋超': [301, '11'], '埃及超': [303, '34'], '南非超': [308, '2'], '约超联': [309, '15'], '香港甲': [311, '13'], '卡塔尔联': [313, '11'], '敘利亚甲': [314, '71'], '阿尔巴超': [315, '15'], '马来超': [316, '22'], '马来甲': [317, '22'], '巴林超': [318, '17'], '摩洛超': [321, '29'], '科威特联': [322, '18'], '利比亚甲': [324, '5'], '黎巴嫩联': [325, '10'], '突尼甲': [326, '25'], '阿曼联': [332, '11'], '英南超': [336, '40'], '苏高联': [337, '34'], '新西兰联': [341, '13'], '斯伐甲': [351, '28'], '波斯甲': [352, '11'], '爱沙甲': [353, '36'], '巴拉甲': [354, '18'], '巴西乙': [358, '38'], '瑞典乙MG': [369, '21'], '瑞典乙OS': [372, '21'], '冰岛甲': [381, '22'], '摩尔甲': [389, '14'], '委内超': [391, '17'], '马其甲': [392, '18'], '智利甲': [415, '34'], '阿乙': [423, '24'], '澳维超': [436, '26'], '法女甲': [440, '11'], '德女联': [441, '21'], '瑞典女超': [443, '22'], '瑞青超': [447, '18'], '美乙': [448, '10'], '澳维女超': [453, '20'], '日职女乙': [455, '14'], '韩联盟': [456, '28'], '日职女甲': [459, '22'], '加拿超': [460, '9'], '丹女甲': [461, '14'], '也门甲': [465, '26'], '哈萨超': [466, '26'], '阿美超': [469, '21'], '挪女超': [473, '18'], '芬女超': [475, '18'], '俄后赛': [476, '18']}'''
match_datas = []
leagues = { '德甲': [8, '34'], '法甲': [11, '38'], 
'西甲': [31, '38'],  '意甲': [34, '38'], '英超': [36, '38'], '英冠': [37, '46']，'荷甲': [16, '34']}
season = ['2017-2018','2018-2019','2019-2020', '2020-2021']
print(len(leagues.keys()))
save_File = pd.read_excel('爬取目标2.xlsx')
start=None
end=None
while start==None or end==None:
    try:
        start=input('输入爬取的开始标号 1 -- 476\n')
        start=int(start)
    except :
        print('输入不对，请输入数字再回车 例如 10 然后回车')
        start=None
        end=None
        continue
    try:
        end=input('输入爬取的结束的标号 1 -- 476\n')
        end=int(end)
    except :
        print('输入不对，请输入数字再回车 例如 10 然后回车')
def get_Match_data(params):
    url = 'https://saishi.zgzcw.com/summary/liansaiAjax.action'
    rsp = requests.post(url=url, headers=headers, data=params)
    data = pd.read_html(rsp.text)[0]
    match_ID = re.findall(reg, rsp.text)
    # print(,match_ID)
    idx = 0
    match_datas = []
    for i in data.iterrows():
        try:
            match_data = [None for i in range(28)]
            match_data[0] = i[1][0]
            match_data[1] = i[1][1]
            match_data[2] = i[1][3]
            res = i[1][2].split(':')
            f = 0
            if int(res[0]) < int(res[1]):
                f = -1
            if int(res[0]) > int(res[1]):
                f = 1
            match_data[3] = f
            match_data[4] = int(res[0])+int(res[1])
            time.sleep(5)
            url2 = 'https://fenxi.zgzcw.com/'+str(match_ID[idx])+'/ypdb'
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
            url4 = 'https://fenxi.zgzcw.com/'+str(match_ID[idx])+'/dxdb'
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
            url3 = 'https://fenxi.zgzcw.com/'+str(match_ID[idx])+'/bjop'
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
            match_datas.append(match_data)
            idx += 1
            time.sleep(5)
        except:
            print('被抓到在爬数据了,装死30秒')
            time.sleep(30)
    return match_datas

have_Download=os.listdir()
for league in leagues.keys():
    if start<=leagues[league][0] and end>=leagues[league][0]:
        for se in season:
            if league+se+'数据.xlsx' in have_Download:
                print(league+se+'数据.xlsx','已经下载过了，以自动跳过')
                continue
            season_datas = []
            match_datas = []
            idx = 0
            save_File = pd.read_excel('爬取目标2.xlsx')
            for roud in range(1, int(leagues[league][1])+1):
                try:
                    st_time = datetime.datetime.now()
                    print('爬取', league, se, roud, '中')
                    params = {'source_league_id': int(leagues[league][0]),
                            'currentRound': roud,
                            'season': se}
                    season_datas.append(get_Match_data(params))
                    print('爬取', league, se, roud, '成功，花费',
                        datetime.datetime.now()-st_time)
                except:
                    print('被抓到在爬数据了,装死30秒')
                    print('爬取', league, se, roud, '失败，花费',
                        datetime.datetime.now()-st_time)
            for roud_data in range(len(season_datas)):
                for m_data in range(len(season_datas[roud_data])):
                    save_File.loc[idx] = season_datas[roud_data][m_data]
                    idx += 1
            save_File.to_excel(league+se+'数据.xlsx')
print('爬取完成')
