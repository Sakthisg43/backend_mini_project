import os
from dotenv import load_dotenv
load_dotenv()

from flask_sqlalchemy import SQLAlchemy

class Config:
    DEBUG = bool(os.getenv('DEBUG',False))
    DEVELOPMENT = bool(os.getenv('DEVELOPMENT',False))
    CSRF_ENABLED = True
    URL_PREFIX = 'api'
    SECRET_KEY = 'Your_secret_string_dev'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    FIXED_RATE = 200
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_PRE_PING = True
    SQLALCHEMY_POOL_RECYCLE = 300
    BUCKET = "pmo-files"
    AWS_DEFAULT_REGION = "ap-south-1"
    AWS_ACCESS_KEY_ID = "AKIAI5MHXOGF72ORW2UQ"
    AWS_SECRET_ACCESS_KEY = "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"
    PORT = os.getenv('PORT') 
    DATETIME_FORMAT =  os.getenv('DATETIME_FORMAT')
    SECRET_KEY =  os.getenv('SECRET_KEY')
    JWT_ALGORITHM  = os.getenv('JWT_ALGORITHM')
    JWT_TOKEN_TIME_OUT_IN_MINUTES = int(os.getenv('JWT_TOKEN_TIME_OUT_IN_MINUTES',5))
    # JWT_TOKEN_TIME_OUT_IN_MINUTES = 2
    JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES = int(os.getenv('JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES',525600))





db =  SQLAlchemy()