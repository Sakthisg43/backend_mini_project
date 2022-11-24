import uuid
from sqlalchemy import Column, DateTime, func, String
from config import Config
from config import db
from sqlalchemy import Column, String, DateTime,create_engine


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
#from sqlalchemy import Column, String, DateTime,VARCHAR,create_engine
def default_uuid():
    return uuid.uuid4().hex

class BaseModel(db.Model):
    __abstract__ = True
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
    id = Column(String(40), primary_key=True, default=lambda: default_uuid())
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), default=None)
    created_by = Column(String(40), default=None)
    updated_by = Column(String(40), default=None)
    deleted_by = Column(String(40), default=None)
