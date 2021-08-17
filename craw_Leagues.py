import requests
import re
import time
leg={}
reg=re.compile(r"""<meta name="keywords" content="(.*?)" />""")
reg2=re.compile(r"""class="em_1">(.*?)</em>""")
for i in range(1,500):
    try:
        url='https://saishi.zgzcw.com/soccer/league/'+str(i)
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
        }
        resp=requests.get(url,headers=headers)
        title=re.findall(reg,str(resp.text))
        roud=re.findall(reg2,str(resp.text))
        if title!=[]:
            title=title[0]
            title=title[:title.index('积')]
            leg[title]=[i,roud[-1]]
    except:
        print(leg)
    time.sleep(5)
print(leg)