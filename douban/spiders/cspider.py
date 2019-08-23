# -*- coding: utf-8 -*-

import re
import scrapy
from douban.items import DetailItem, CommitItem
from scrapy.exceptions import DropItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/tag/?icn=index-nav']

    rules = (
        # <-------------------------跳板一---------------------->
        # https://book.douban.com/tag/中国文学
        Rule(LinkExtractor(restrict_xpaths='//*[@id="content"]/div/div[1]/div[2]/div[1]/table/tbody/tr[2]/td[1]', unique=True), process_links='process_book_links', follow=True),
        # https://book.douban.com/tag/中国文学?start=0&type=T
        # 调用process_book_links拼凑request_url得到跳板首页数据
        # <-------------------------跳板一---------------------->
        # 小说翻页
        Rule(LinkExtractor(restrict_xpaths='//span[@class="next"]'),process_links='process_book_links', follow=True),
        # 小说详情页
        # 按restrict_xpaths匹配到的是一个url列表，会将callback作用于所有url之上
        # 这个就类似于python里的map函数  map(func, iter)
        # follow=True表示在调用回调函数之后继续按下一个Rule对象提取链接
        Rule(LinkExtractor(restrict_xpaths='//li[@class="subject-item"]/div[@class="pic"]'), callback='parse_book_detail', follow=True),

        # 小说书评链接页[此外还包括短评、读书笔记等分类]
        # https://book.douban.com/subject/2567698/reviews
        # <-------------------------跳板二---------------------->
        # Rule(LinkExtractor(allow=r'/reviews$'), process_links='process_commit_links', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//section[@class="reviews mod book-content"]//span[@class="pl"]', unique=True), process_links='process_commit_links', follow=True),
        # https://book.douban.com/subject/2567698/reviews?start=20
        # 调用process_book_links拼凑request_url得到跳板首页数据
        # <-------------------------跳板二---------------------->
        # 小说书评翻页
        Rule(LinkExtractor(restrict_xpaths='//div[@class="paginator"]/span[@class="next"]', unique=True), process_links='process_commit_links', follow=True),
        # 小说书评详情页
        Rule(LinkExtractor(restrict_xpaths='//div[@class="main review-item"]//div[@class="main-bd"]/h2', unique=True), callback='parse_commit_detail'),
    )


    #   <-----------------------------------小说----------------------------------->
    # 这一部分也可以采取process_commit_links的方法进行字符串拼接
    # 构造request_url。但是学习一种新的解决办法也挺好
    @staticmethod
    def process_book_links(links):
        '''
        :param links:  [Link(url='https://book.douban.com/tag/中国文学?start=20&type=T', text='后页>', fragment='', nofollow=False)]
        :param dir(link): ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', 'fragment', 'nofollow', 'text', 'url']
        :return:
        '''
        for link in links:
            link_url = links[0].url
            if 'start' not in link_url:
                link.url = link_url + '?start=0&type=T'
                yield link
            else:
                numb = int(re.findall(r'.*?start=(\d+).*', link_url)[0])
                if numb < 1000:  # 1000表示书本数量，本标签下最多只有1000本
                    yield link


    # 解析小说详细数据
    def parse_book_detail(self, response):
        item = DetailItem()
        item['book_title'] = response.xpath('//div[@id="wrapper"]//span/text()').get()
        item['book_img_url'] = response.xpath('//div[@id="content"]//div[@id="mainpic"]/a[@class="nbg"]/@href').get()
        item['book_commit'] = response.xpath('//div[@class="rating_self clearfix"]/strong/text()').get().strip()
        item['book_commit_numb'] = ''.join(response.xpath('//div[@class="rating_sum"]/span/a//text()').getall())
        item['book_intro'] = ''.join(response.xpath('//div[@id="link-report"]//div[@class="intro"]//text()').getall())
        item['book_author_intro'] = ''.join(response.xpath('//div[@class="indent " and not(@id)]//div[@class="intro"]//text()').getall())
        dc_lis = response.xpath('//div[@id="info"]//text()').getall()
        cc_lis = list(map(lambda x:re.sub('[\n\s:]', '', x), dc_lis))
        va_lis = [val for val in cc_lis if val!='']
        nva_lis = list(map(lambda x: x.replace('统一书号', 'ISBN') if x == '统一书号' else x, va_lis))  # 统一书号ISBN
        item['book_author'] = ''.join(nva_lis[nva_lis.index('作者')+1:nva_lis.index('出版社'):])
        item['book_pub'] = nva_lis[nva_lis.index('出版社')+1]
        if '出品方' in nva_lis:
            item['book_producer'] = nva_lis[nva_lis.index('出品方')+1]
        else:
            item['book_producer'] = '无出品方'
        if '副标题' in nva_lis:
            item['book_subtitle'] = nva_lis[nva_lis.index('副标题')+1]
        else:item['book_subtitle'] = '无副标题'
        if '丛书' in nva_lis:
            item['book_series'] = nva_lis[nva_lis.index('丛书')+1]
        else:
            item['book_series'] = '无丛书分类'
        if '页数' in nva_lis:
            item['book_page'] = ''.join(re.findall(r'(.*?)页?', nva_lis[nva_lis.index('页数') + 1])) + '页'
        else:
            item['book_page'] = '{0}为套装书，无详细页码信息'.format(item['book_title'])
        item['book_date'] = nva_lis[nva_lis.index('出版年')+1]
        item['book_price'] = nva_lis[nva_lis.index('定价')+1]
        item['book_bind'] = nva_lis[nva_lis.index('装帧')+1]
        item['book_isbn'] = nva_lis[-1]
        return item


    #   <-----------------------------------书评----------------------------------->
    @staticmethod
    def process_commit_links(links):
        for link in links:
            link_url = links[0].url
            if 'start' not in link_url:
                link.url = link_url + '?start=0'
                # print('it is here 跳板首页{}'.format(link.url))
                yield link
            else:
                numb = int(re.findall(r'.*?start=(\d+)', link_url)[0])
                # print('it is here 翻页操作{}'.format(link_url))
                if numb < 20:  # 获取前五页的书评
                    yield link


    # 解析书评详细信息
    def parse_commit_detail(self, response):
        print(response.url)
        item = CommitItem()
        print('commit_url->', response.url)
        item['commit_title'] = response.xpath('//div[@id="content"]//div[@class="article"]/h1/span/text()').get()
        item['commit_uurl'] = response.xpath('//div[@id="content"]//div[@class="main"]/a/@href').get()
        item['commit_uname'] = response.xpath('//div[@id="content"]//header[@class="main-hd"]/a[1]/span/text()').get()
        item['commit_bktitle'] = response.xpath('//div[@id="content"]//header[@class="main-hd"]/a[2]/text()').get()
        item['commit_score'] = response.xpath('//span[@class="main-title-hide"]/text()').get()
        item['commit_time'] = response.xpath('//span[@class="main-meta"]/text()').get()
        other_comm = response.xpath('//div[@id="review-content"]/@data-ad-ext').get()
        item['commit_gdcomm'] = other_comm.split('·')[0].strip()
        item['commit_bdcomm'] = other_comm.split('·')[1].strip()
        item['commit_content'] = response.xpath('//div[@class="review-content clearfix"]//text()').getall()
        return item


