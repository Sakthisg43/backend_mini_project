from sqlalchemy import Column, String, DateTime,Float,JSON,Integer,Text,Boolean
from base import BaseModel
'''engine = create_engine('postgresql://postgres:postgres@localhost:5432/')
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()'''

class Project(BaseModel):
    __tablename__ = 'project'
    # project_id = db.Column(db.Integer, primary_key=True)
    title = Column(String(255))
    tm_fixed_cost = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    duration = Column(Integer)
    resources = Column(JSON)
    logo_url = Column(String(200))
    overall_completion = Column(Integer)


class User(BaseModel):
    __tablename__ = 'user_data'

    first_name = Column(String(50), nullable=True)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(Text)
    email_verified =  Column(Boolean())
    password = Column(String(100))


class TempUser(BaseModel):
    __tablename__ = 'temp_user'

    user_id = Column(String(40))
    device_id = Column(Text)




'''class Project_Group(BaseModel):
    __tablename__ = 'project_group'
    group_name = db.Column(db.String)

class Project_Group_Project(BaseModel):
    __tablename__ = 'project_group_project'
    project_id =  db.Column(db.Integer)
    project_group_id = db.Column(db.Integer)'''

