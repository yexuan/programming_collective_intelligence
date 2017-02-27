#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2017/2/26 16:14 
# @Author : Shuqi.qin
# @File : recommendations.py 
# @Software: PyCharm

import time
from pydelicious import get_popular, get_urlposts, get_userposts


# 构建用户字典，其中每一项都各自指向一个等待填入具体url的空字典
def initializeUserDict(tag, count=5):
    user_dict = {}
    # 获取某tag下前count个最受欢迎的url post记录
    for p1 in get_popular(tag=tag)[0:count]:
        # 获取所有post该url的用户
        for p2 in get_urlposts(p1['href']):
            user = p2['user']
            user_dict[user] = {}
    return user_dict


def fillItems(user_dict):
    all_items = {}
    # 查找所有用户都post过的url
    for user in user_dict.keys():
        for i in range(3):
            try:
                posts = get_userposts(user)
                break
            except:
                print "Failed user " + user + ",retrying"
                time.sleep(4)
        for post in posts:
            url = post['href']
            user_dict[user][url] = 1.0
            all_items[url] = 1
    # 用0填充缺失的项
    for ratings in user_dict.values():
        for item in all_items.keys():
            if not ratings.has_key(item):
                ratings[item] = 0.0
