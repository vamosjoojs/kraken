import os
import uuid
from io import BytesIO

import boto3
import requests
from botocore.config import Config
from botocore.exceptions import ClientError

from app.config.config import config


class S3Service:
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name='us-east-2'
        )
        self.s3 = self.session.resource('s3')
        self.bucket = self.s3.Bucket(config.AWS_BUCKET_NAME)

    def upload_file(self, file, key_name):
        with open(file, 'rb') as fh:
            buf = BytesIO(fh.read())

        self.bucket.upload_fileobj(buf, key_name)

        bucket_location = boto3.client('s3').get_bucket_location(Bucket=config.AWS_BUCKET_NAME)

        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location['LocationConstraint'],
            config.AWS_BUCKET_NAME,
            key_name)

        return object_url

    @staticmethod
    def download_file_url(key: str, ):
        clip_name = f'{str(uuid.uuid4())}.mp4'
        output_path = os.path.join(os.getcwd(), 'download')

        output_file = os.path.join(output_path, clip_name)

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        r = requests.get(key, allow_redirects=True)
        open(output_file, 'wb').write(r.content)
        return output_file

    def create_presigned_url(self, object_name, expiration=3600):
        s3_client = boto3.client('s3',
                                 region_name='us-east-2',
                                 aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                                 config=Config(signature_version='s3v4'))
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': config.AWS_BUCKET_NAME,
                                                                'Key': object_name},
                                                        ExpiresIn=expiration)
        except ClientError as e:
            return None

        return response
