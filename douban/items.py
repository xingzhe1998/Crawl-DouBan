# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DetailItem(Item):
    # define the fields for your item here like:
    book_type = "中国文学"       # 书本分类
    book_commit = Field()       # 评价分数
    book_commit_numb = Field()  # 评价人数
    book_pub = Field()          # 书本出版社  !
    book_intro = Field()        # 书本简介
    book_bind = Field()         # 书本装帧
    book_isbn = Field()         # 书本ISBN号
    book_page = Field()         # 书本页数    !
    book_series = Field()       # 书本丛书    !
    book_producer = Field()     # 书本出品方  !
    book_subtitle = Field()     # 书本副标题  !
    book_title = Field()
    book_img_url = Field()
    book_author = Field()
    book_author_intro = Field()
    book_date = Field()
    book_price = Field()


class CommitItem(Item):
    commit_title = Field()          # 书评标题
    commit_bktitle = Field()        # 书评对象 -> 书名
    commit_uname = Field()          # 用户名
    commit_uurl = Field()           # 书评用户个人主页链接
    commit_gdcomm = Field()         # 别人对本书评 -> 支持
    commit_bdcomm = Field()         # 别人对本书评 -> 反对
    commit_score = Field()
    commit_time = Field()
    commit_content = Field()
