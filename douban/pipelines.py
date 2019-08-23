# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import pymongo

# 清洗
class DoubanPipeline(object):
    def process_item(self, item, spider):
        # DetailItem
        if item.__class__.__name__ == 'DetailItem':
            if item['book_author_intro']:
                dai_lis = list(map(lambda x:re.sub('[\n\s]', '', x) ,item['book_author_intro']))
                item['book_author_intro'] = ''.join(dai_lis)[:100] + '...'
            else:
                item['book_author_intro'] = '暂无作者简介'
            if item['book_intro']:
                db_lis = list(map(lambda x:re.sub('[\n\s]', '', x) ,item['book_intro']))
                item['book_intro'] = ''.join(db_lis)[:100] + '...'
            else:
                item['book_intro'] = '暂无书本简介'

            item['book_commit'] += '分'
            item['book_price'] = ''.join(re.findall(r'(.*?)元?', item['book_price'])) + '元'
            if '-' in item['book_date']:
                date_lis = item['book_date'].split('-')
                if len(date_lis) == 3:
                    year, month, day = date_lis
                    item['book_date'] = year+'年'+month+'月'+day+'日'
                else:
                    year, month = date_lis
                    item['book_date'] = year+'年'+month+'月'
            else:pass

        # CommitItem
        else:
            commit_content = '\n'.join([val for val in list(map(lambda x:re.sub('[\n\s]', '', x), item['commit_content'])) if val!=''])
            item['commit_content'] = commit_content
        return item

# 入库
class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        print('正在插入mongodb...')
        if item.__class__.__name__ == 'DetailItem':
            self.db['DetailItem'].insert_one(dict(item))
        else:
            self.db['CommitItem'].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
