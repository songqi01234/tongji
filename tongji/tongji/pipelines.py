# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from scrapy.conf import settings


# class TongjiPipeline(object):
#     def process_item(self, item, spider):
#         with open('2.txt', 'a', encoding='utf-8') as f:
#             f.write(json.dumps(item,ensure_ascii=False,indent=2))
#         # return item

# 将爬取到的信息插入到MySQL数据库中
class TongjiPipeline(object):
    def process_item(self, item, spider):
        host = settings['MYSQL_HOSTS']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DB']
        c = settings['CHARSET']
        port = settings['MYSQL_PORT']
        # 数据库连接
        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
        # 数据库游标
        cue = con.cursor()
        print("mysql connect succes")  # 测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        try:
            cue.execute(
                "insert into tongji (sheng,shi,shibianma,quxian,quxianbianma,jiedao,jiedaobianma,weiyuanhui,weiyuanhuibianma) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                [item['sheng'], item['shi'], item['shibianma'], item['quxian'], item['quxianbianma'], item['jiedao'],
                 item['jiedaobianma'], item['weiyuanhui'], item['weiyuanhuibianma']])
            print("insert success")  # 测试语句
        except Exception as e:
            print('Insert error:', e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item
