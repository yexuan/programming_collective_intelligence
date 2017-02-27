#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/2/26 16:19
# @Author : Shuqi.qin
# @Site :
# @File : rec_test.py
# @Software: PyCharm

import random
import making_recommendations.deliciousrec as dr
import making_recommendations.recommendations as rc

del_users = dr.initializeUserDict('programming')
del_users['tsegaran'] = {}
dr.fillItems(del_users)

# 随机选择一个用户，寻找与其品味相似的其他用户
user = del_users.keys()[random.randint(0,len(del_users)-1)]
similar_users = rc.topMatches(del_users,user)

# 为该用户推荐链接

rec_urls = rc.getRecommendationsBaseOnPersonSimilarity(del_users,user)

# 寻找与某一链接最类似的链接list
url = rec_urls[0][1]
similar_urls = rc.topMatches(rc.transformPrefs(del_users),url)

print 'over'


