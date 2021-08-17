#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql

# 创建连接
conn = pymysql.connect(host='23.95.230.155', port=3306, user='whatcoldwind', passwd='liao520520', db='football_database')
# 创建游标
cursor = conn.cursor()
cmd='''SELECT `Source.Name`, `Column1`, `时间`, `主队`, `客队`, `赛果`, `总进球`, `主初赔`, `客初赔`, `初盘`, `主临赔`, `客临盘赔`, `临盘`, `主胜概率`, `客胜概率`, `大球初盘`, `小球初盘`, `球初盘`, `大球临盘`, `小球临盘`, `球临盘`, `欧主初赔`, `欧客初赔`, `欧初平赔`, `欧主临赔`, `欧客临赔`, `欧平临赔`, `欧主概率`, `欧平概率`, `欧客概率`, `大球盘变化`, `大球赔变化`, `小球赔变化`, `让盘变化`, `亚主赔变化`, `亚客赔变化`, `欧主赔变化`, `欧客赔变化`, `欧平赔变化` FROM `football_sheet` WHERE 
`主初赔` AND `客初赔` AND `初盘` AND `主临赔` AND `客临盘赔` AND `临盘` AND `主胜概率` AND `客胜概率` AND `大球初盘` AND `小球初盘`
     AND `球初盘` AND `大球临盘` AND `小球临盘` AND `球临盘` AND `欧主初赔` AND `欧客初赔` AND `欧初平赔` AND `欧主临赔` AND `欧客临赔`
     AND `欧平临赔` AND `欧主概率` AND `欧平概率` AND `欧客概率` AND `大球盘变化` AND `大球赔变化` AND `小球赔变化` AND `让盘变化` AND 
     `亚主赔变化` AND `亚客赔变化` AND `欧主赔变化` AND `欧客赔变化` AND `欧平赔变化`'''
cursor.execute(cmd)

# 获取第一行数据
row_1 = cursor.fetchone()
print(row_1)
row_1 = cursor.fetchone()
print(row_1)
conn.commit()
cursor.close()
conn.close()