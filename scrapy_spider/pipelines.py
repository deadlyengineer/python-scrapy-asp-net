# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from scrapy_spider.models import JobsDB, db_connect, create_table
#from scrapy.exceptions import DropItem
from .models import *

class ScrapySpiderPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(engine)
        #self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        jobs_db = JobsDB(**item)

        try:
            session.add(jobs_db)
            session.commit()
        except IntegrityError:
            session.rollback()
        finally:
            session.close()

        return item
