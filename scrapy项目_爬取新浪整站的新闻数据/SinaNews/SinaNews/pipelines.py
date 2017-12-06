# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class SinanewsPipeline(object):
    def process_item(self, item, spider):
        item = dict(item)
        if item['title']:
            title = item['title'][0].strip()
            path = item['child_path'] + '/' + title + '.txt'
            content = item['content']
            with open(path,'wb')as f:
                f.write(content.encode("utf-8"))
        return item
