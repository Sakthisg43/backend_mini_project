import uuid
from sqlalchemy import JSON, Column, String,Integer,Float,DateTime,Boolean,Text,VARCHAR
from base import BaseModel

def generate_uuid():
    return str(uuid.uuid4())

#database model for weekly_reports


class Weekly_reports(BaseModel):
    __table_name__ = "weekly_reports"
    project_id = Column(VARCHAR(40),nullable=True)
    t_m_and_fixed_cost = Column(Integer)
    resources = Column(JSON)
    weekly_completion = Column(Integer)
    no_storeis = Column(Integer)
    features_completed = Column(Integer)
    new_bugs = Column(Integer)
    bug_fixed = Column(Integer)
    is_code_review = Column(Boolean)
    is_unit_testing = Column(Boolean)
    is_weekly_communication = Column(Boolean)
    delay= Column(Integer)
    
    
class Other_weekly_reports_data(BaseModel):
    __table_name__ = "other_weekly_reports_data"
    dependencies = Column(Text)
    risk = Column(Text)
    risk_mitigation = Column(Text)
    support_required  = Column(Text)
    weekly_report_id = Column(String)