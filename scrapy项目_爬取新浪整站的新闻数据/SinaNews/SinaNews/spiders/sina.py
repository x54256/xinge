# -*- coding: utf-8 -*-
import scrapy,os
from SinaNews.items import SinanewsItem

class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items=[]
        BASEPATH = "E:/sina"
        parentTitle = response.xpath('//h3[@class="tit02"]//text()').extract()[0:-10]
        parentUrls = response.xpath('//h3[@class="tit02"]//@href').extract()[0:-7]
        subTitle = response.xpath('//ul[@class="list01"]/li/a/text()').extract()
        subUrls = response.xpath('//ul[@class="list01"]/li/a/@href').extract()
        for i in range(len(parentTitle)):
            if not os.path.exists(BASEPATH + '/' + parentTitle[i]):
                os.makedirs(BASEPATH + '/' + parentTitle[i])
            for j in range(len(subTitle)):
                # print(len(subTitle),len(parentTitle),parentUrls)
                # print(parentUrls[i],i)
                # print(subUrls[j],j)
                if subUrls[j].startswith(parentUrls[i]):
                    item = SinanewsItem()
                    item['parentTitle'] = parentTitle[i]
                    item['parentUrls'] = parentUrls[i]
                    item['subTitle'] = subTitle[j]
                    item['subUrls'] = subUrls[j]
                    child_path = BASEPATH + '/' + parentTitle[i] + '/' + subTitle[j]
                    item['child_path'] = child_path
                    if not os.path.exists(child_path):
                        os.makedirs(child_path)
                    items.append(item)
                    yield scrapy.Request(item['subUrls'],callback=self.second_parse,meta={"item":item})

    def second_parse(self,response):
        SonList = response.xpath("//a/@href").extract()
        item = response.meta['item']
        for i in SonList:
            if i.startswith(item['parentUrls']):
                item['SonUrl'] = i
                yield scrapy.Request(i,callback=self.last_parse,meta={"item":item})


    def last_parse(self,response):
        item = response.meta['item']
        item['title'] = response.xpath('//h1[@id]/text() | //h1[@id]/font/text()').extract()
        content_list = response.xpath('//div[@id=\"artibody\"]/p/text()').extract()
        item['content'] = ''.join(content_list).strip()
        yield item










