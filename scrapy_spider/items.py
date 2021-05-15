# -*- coding: utf-8 -*-
# Define here the models for your scraped items
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst

class JobsItem(scrapy.Item):
    
    url = scrapy.Field(output_processor = TakeFirst())
    title = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    workplace = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    type_of_employment = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    working_hours = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    mode_of_operation = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    accomodation = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    required_workers = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    transportation_fee = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    start_date = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    end_date = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    education_level = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    work_experience = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    other_information = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    employer = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    contact = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    driving_test = scrapy.Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())