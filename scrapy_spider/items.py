# -*- coding: utf-8 -*-
# Define here the models for your scraped items
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst

class JobsItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(input_processor = MapCompose(str.strip), output_processor=TakeFirst())
    source = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    employer = scrapy.Field(input_processor = MapCompose(str.strip), output_processor=TakeFirst())
    workplace = scrapy.Field(input_processor = MapCompose(str.strip), output_processor=TakeFirst())
    start_date = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    end_date = scrapy.Field(input_processor = MapCompose(str.strip), output_processor=TakeFirst())
    category = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    description1 = scrapy.Field(input_processor = MapCompose(str.strip), output_processor=TakeFirst())
    description2 = scrapy.Field(input_processor = MapCompose(str.strip), output_processor=TakeFirst())

    requirements = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    benefits = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
