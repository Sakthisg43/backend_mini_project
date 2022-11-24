import boto3
from config import Config
def upload_to_s3(name,obj=None):
    try:
        client = boto3.client(
        's3',
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_DEFAULT_REGION)
        client.put_object(Body=obj, Bucket=Config.BUCKET, Key=name , ACL = "public-read")

        return True
    except Exception as e:
        print("error",e)

        return False

