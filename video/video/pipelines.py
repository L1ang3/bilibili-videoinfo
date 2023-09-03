# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class VideoPipeline:
    def __init__(self):
        self.nums = 0
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        # 指定数据库
        mydb = client['bilibili']
        # 存放数据的数据库表名
        self.collection = mydb['data_2']

    def process_item(self, item, spider):
        data = dict(item)
        self.collection.insert_one(data)
        self.nums += 1
        print('Successful getting:'+str(self.nums)+'!  '+item['title'])
        return item
