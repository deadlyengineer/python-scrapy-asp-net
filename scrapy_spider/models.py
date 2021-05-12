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
    source = Column('Source', String(1024))
    employer = Column('Employer', String(1024))
    workplace = Column('Workplace', String(1024))
    start_date = Column('Start_date', String(1024))
    end_date = Column('End_date', String(256))
    category = Column('Category', String(256))
    description1 = Column('Description1', Text())
    description2 = Column('Description2', Text())
    requirements = Column('Requirements', Text())
    benefits = Column('Benefits', Text())
