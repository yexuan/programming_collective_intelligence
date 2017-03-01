#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 01/03/2017 11:57 AM 
# @Author : Shuqi.qin 
# @File : test.py 
# @Software: PyCharm Community Edition

import clusters

blognames, words, data = clusters.readfile('blogdata.txt')

cluster = clusters.hclusters(data)

clusters.drawdendrogram(cluster, blognames, 'wordcluster.jpg')

