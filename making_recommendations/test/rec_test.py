#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2017/2/26 16:19 
# @Author : Shuqi.qin 
# @Site :  
# @File : test.py
# @Software: PyCharm

import making_recommendations.recommendations as rc


res1 = rc.sim_distance(rc.critics,"Lisa Rose","Gene Seymour")

res2 = rc.sim_pearson(rc.critics,"Lisa Rose","Gene Seymour")

res3 = rc.topMatches(rc.critics,"Toby",n=3)

res4 = rc.getRecommendationsBaseOnPersonSimilarity(rc.critics,"Toby")

print 'over'

import making_recommendations.pydelicious as pydelicious

print pydelicious.get_popular(tag='programming')