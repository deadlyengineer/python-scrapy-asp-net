#from scrapy.utils.project import get_project_settings
from sqlalchemy.engine import create_engine
#from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, Date, Boolean, Text)

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class JobsDB(DeclarativeBase):
    __tablename__ = "burzarada_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column('URL', String(256), unique=True)
    title = Column('Title', String(1024))
    workplace = Column('Workplace', String(1024))
    type_of_employment = Column('Type_of_employment', String(1024))
    working_hours = Column('Working_hours', String(1024))
    mode_of_operation = Column('Mode_of_operation', String(1024))
    accomodation = Column('Accomodation', String(1024))
    required_workers = Column('Required_workers', String(1024))
    transportation_fee = Column('Transportation_fee', String(1024))
    start_date = Column('Start_date', String(256))
    end_date = Column('End_date', String(256))
    education_level = Column('Education_level', String(1024))
    work_experience = Column('Work_experience', String(1024))
    other_information = Column('Other_information', Text())
    employer = Column('Employer', String(1024))
    contact = Column('Contact', String(1024))
    driving_test = Column('Driving_test', String(1024))

