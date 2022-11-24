from base import BaseModel
from sqlalchemy import Column,String,Boolean

class User(BaseModel):
    
    __tablename__ = "user_table"
    name = Column(String(255))
    email = Column(String(255))
    is_super_admin = Column(Boolean, nullable=False)
    delete_permission = Column(Boolean, nullable=False)
    edit_permission = Column(Boolean, nullable=False)
    password_hash = Column(String(255))

