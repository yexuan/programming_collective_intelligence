#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2017/2/26 16:14 
# @Author : Shuqi.qin
# @File : recommendations.py 
# @Software: PyCharm

# A dictionary of movie critics and their ratings of a small
# set of movies
critics={\
    'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},\
    'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},\
    'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,'Superman Returns': 3.5, 'The Night Listener': 4.0},\
    'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},\
    'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,'You, Me and Dupree': 2.0}, \
    'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},\
    'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}\
    }

from math import sqrt

#返回两个用户的评价相似度（欧几里德距离）
def sim_distance(prefs,person1,person2):
    #share_item列表
    si = dict([(item,1) for item in prefs[person1] if item in prefs[person2]])
    if len(si)==0:
        return 0
    #计算所有差值的平方和
    distance = sum([pow(prefs[person2][item]-prefs[person1][item],2) for item in si.keys()])
    return 1.0/(1+sqrt(distance))

#返回两个用户的评价相似度（皮尔逊相关系数）
def sim_pearson(prefs,person1,person2):
    #share_item列表
    si = dict([(item,1) for item in prefs[person1] if item in prefs[person2]])
    if len(si) == 0:
        return 0
    #对每个用户的所有评分求和
    sum1 = sum(prefs[person1][item] for item in si)
    sum2 = sum(prefs[person2][item] for item in si)

    # 对每个用户的所有评分求平方和
    sum1Sq = sum(pow(prefs[person1][item],2) for item in si)
    sum2Sq = sum(pow(prefs[person2][item],2) for item in si)

    # 求评分的乘积和
    pSum = sum(prefs[person1][item]*prefs[person2][item] for item in si)

    # 计算皮尔逊系数
    num = pSum - float(sum1*sum2)/len(si)
    den = sqrt((sum1Sq-pow(sum1,2)/len(si))*(sum2Sq-pow(sum2,2)/len(si)))

    if den == 0:
        return 0
    return float(num)/den

# 返回相似用户列表，相似度由高到低排序
# 返回结果的个数与相似度计算算法均为可选参数
def topMatches(prefs,person,n=5,sim_func=sim_pearson):
    scores = [(sim_func(prefs,person,other),other) for other in prefs.keys() if other != person]
    # 对列表进行排序 相似度最高的排在最前面
    scores.sort(reverse=True)
    return scores[0:n]


# 基于用户相似度为用户推荐物品
def getRecommendationsBaseOnPersonSimilarity(prefs,person,sim_func=sim_pearson):
    totals = {}
    sim_sum = {}

    for other in prefs.keys():
        if other == person:
            continue
        sim  = sim_func(prefs,person,other)

        # 忽略相似度小于等于0的情况
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item in prefs[person] and prefs[person][item] != 0:
                continue
            totals.setdefault(item,0)

            # 相似度*分数
            totals[item] += sim*prefs[other][item]

            # 相似度之和
            sim_sum.setdefault(item,0)
            sim_sum[item] += sim

    # 建立一个归一化列表
    rankings = [(float(totals[item])/sim_sum[item],item) for item in totals]

    rankings.sort(reverse=True)

    return rankings

def transformPrefs(prefs):
    result = {}
    for person in prefs.keys():
        for item in prefs[person].keys():
            result.setdefault(item,{})
            # 用户和物品转置
            result[item][person] = prefs[person][item]
    return result
