from datetime import datetime
from database import Base
from sqlalchemy import Integer, Column, String, DateTime, func

class Urls(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True,autoincrement=True ,index=True)
    url =  Column(String)
    short_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    access_count = Column(Integer, default=0)

