import boto3
from app.config.config import config


def upload_file(file, key_name):
    s3_bucket_name = config.AWS_BUCKET_NAME

    s3 = boto3.client('s3',
                      aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)
    
    object_url = "https://{}.s3.amazonaws.com/{}".format(s3_bucket_name, key_name)

    s3.upload_fileobj(file, s3_bucket_name, key_name)

    return object_url
