#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 03/03/2017 1:07 PM 
# @Author : Shuqi.qin 
# @File : data_source.py 
# @Software: PyCharm Community Edition

# 导入:
from sqlalchemy import Column, create_engine,BIGINT,VARCHAR,TIMESTAMP,Integer,String,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义QueryList对象,存储用户的查询词
class QueryList(Base):
    # 表的名字:
    __tablename__ = 'query_list'

    # 表的结构:
    query_id = Column(BIGINT, primary_key=True)
    query = Column(VARCHAR(1000))
    count = Column(BIGINT)
    log_time = Column(TIMESTAMP)


# 定义ProductList对象，存储有点击的suggestion条目
class ProductList(Base):
    __tablename__ = 'click_item'
    product_id = Column(BIGINT, primary_key=True)
    original_id = Column(VARCHAR(1000))
    product_title = Column(VARCHAR(1000))
    business_type = Column(String(20))
    log_time = Column(TIMESTAMP)






# 存储查询点击映射关系
class ClickInfoList(Base):
    __tablename__ = 'click_info'
    query_id = Column(BIGINT, primary_key=True)
    product_id = Column(BIGINT, primary_key=True)
    click_loc = Column(Integer)
    click_count = Column(Integer)
    log_time = Column(TIMESTAMP)


# 定义hiddenNode对象，存储隐藏层结点
class HiddenNode(Base):
    __tablename__ = 'hidden_node'
    node_id = Column(BIGINT, primary_key=True)
    log_time = Column(TIMESTAMP)


class QueryHidden(Base):
    __tablename__ = 'query_hidden'
    from_id = Column(BIGINT, primary_key=True)
    to_id = Column(BIGINT, primary_key=True)
    strength = Column(Float, primary_key=True)


class HiddenProduct(Base):
    table_name = 'hidden_product'
    from_id = Column(BIGINT, primary_key=True)
    to_id = Column(BIGINT, primary_key=True)
    strength = Column(Float, primary_key=True)

# 初始化数据库连接:
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/test')

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

#往数据库表中添加一行记录：
# 创建session对象:
session = DBSession()
# 创建新User对象:
new_user = User(id='5', name='Bob')
# 添加到session:
session.add(new_user)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()