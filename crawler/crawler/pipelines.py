# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class ProductPipeline(object):

    def __init__(self):
        self.writer = csv.DictWriter(open("dataset.csv", "w"), fieldnames=("title", "category", "description"))
        self.writer.writeheader()

    def process_item(self, item, spider):
        product = dict(item)
        self.writer.writerow(product)