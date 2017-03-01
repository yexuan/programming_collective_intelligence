#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 01/03/2017 9:55 AM 
# @Author : Shuqi.qin 
# @File : clusters.py 
# @Software: PyCharm Community Edition


from math import sqrt
from PIL import Image, ImageDraw


def readfile(filename):
    lines = [line for line in file(filename)]

    # First line is the column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def pearson(v1, v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0: return 0

    return 1.0 - num / den


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


def hclusters(rows, distance=pearson):
    # 用于缓存组群距离，减少运算量
    distances = {}
    currentclustid = -1

    clusters = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clusters) > 1:
        lowestpair = (0, 1)
        closest = distance(clusters[0].vec, clusters[1].vec)

        for i in xrange(len(clusters)):
            for j in xrange(i + 1, len(clusters)):
                if (clusters[i].id, clusters[j].id) not in distances.keys():
                    distances[(clusters[i].id, clusters[j].id)] = distance(clusters[i].vec, clusters[j].vec)
                if distances[(clusters[i].id, clusters[j].id)] < closest:
                    closest = distances[(clusters[i].id, clusters[j].id)]
                    lowestpair = (i, j)

        mergeVec = [float(clusters[lowestpair[0]].vec[i] + clusters[lowestpair[1]].vec[i]) / 2.0 for i in range(len(clusters[lowestpair[0]].vec))]

        # 生成新的聚类
        newCluster = bicluster(mergeVec, left=clusters[lowestpair[0]].id, right=clusters[lowestpair[1]].id,
                               distance=closest, id=currentclustid)

        # 非叶结点的id为负数
        currentclustid -= 1
        del clusters[lowestpair[1]]
        del clusters[lowestpair[0]]
        clusters.append(newCluster)

    return clusters[0]


def printclust(clust, labels=None, n=0):
    # 利用缩进来达到层级布局
    for i in range(n): print ' ',
    if clust.id < 0:
        # id为负表示这是一个分支
        print '-'
    else:
        # id为正表示这是一个叶结点（blog）
        if labels is None:
            print clust.id
        else:
            print labels[clust.id]

    # 递归函数打印左侧和右侧分支
    if clust.left is not None: printclust(clust.left, labels=labels, n=n + 1)
    if clust.right is not None: printclust(clust.right, labels=labels, n=n + 1)


def getheight(clust):
    # 叶子结点的高度为1
    if clust.left == None and clust.right == None: return 1

    # 反之高度为左右分支高度之和
    return getheight(clust.left) + getheight(clust.right)


def getdepth(clust):
    # 叶子结点的深度为0
    if clust.left == None and clust.right == None: return 0

    # 聚合结点的深度为左右分支中深度较大者再加上聚合结点的距离
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance


# 为聚类创建图片
def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    # 高度和宽度
    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)

    # 宽度是固定的，所以需要对距离做出适当调整
    scaling = float(w - 150) / depth

    # 创建一个白色背景的图片
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

    # Draw the first node
    drawnode(draw, clust, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')


# 输入参数：聚类结点，结点高度
# 功能：计算结点位置，用线条将他们连接起来
def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        # 线长度
        ll = clust.distance * scaling
        # 聚类到子节点的垂直线
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))

        # 连接左侧结点的水平线
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))

        # 连接右侧结点的水平线
        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0, 0))

        # 递归
        drawnode(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
        drawnode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
    else:
        # 绘制叶子结点标签
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))
