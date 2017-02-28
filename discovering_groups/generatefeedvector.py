#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/2/26 16:19
# @Author : Shuqi.qin
# @Site :
# @File : rec_test.py
# @Software: PyCharm

import feedparser
import re



# 提取文章中的单词列表
def getWords(html):
    # type: (object) -> object
    # 去除所有的html标记
    text = re.compile(r'<[^>]+>').sub('', html)

    # 利用所有非字母字符分割单词
    words = re.compile(r'[^a-z^A-Z]+').split(text)

    # 转化为小写形式
    return [word.lower() for word in words]


# 返回一个RSS订阅源的标题及包含单词技术情况的字典
# to do:添加中文分词
def getWordsCount(url):
    # 解析订阅源
    d = feedparser.parse(url)
    wc = {}

    # 遍历所有的文章条目
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
        words = getWords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return d.feed.title, wc


apcount = {}
wordscount = {}
feedlist = [line.strip() for line in open('feedlist.txt')]

for url in feedlist:
    try:
        title, wc = getWordsCount(url)
        wordscount[title] = wc
        for word,count in wc.items():
            apcount.setdefault(word,0)
            if count > 1:
                apcount[word] += 1
    except:
        print 'Failed to parse feed %s' % url


wordlist = []

for word,count in apcount.items():
    frac = float(count)/len(feedlist)
    if frac>0.1 and frac<0.5:
        wordlist.append(word)

out=file('blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordscount.items():
  print blog
  out.write(blog)
  for word in wordlist:
    if word in wc: out.write('\t%d' % wc[word])
    else: out.write('\t0')
  out.write('\n')