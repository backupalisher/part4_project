import logging

import boto3
from botocore.exceptions import ClientError

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

BucketName = 'part4images'


def get_list():
    for key in s3.list_objects(Bucket=BucketName)['Contents']:
        print(key['Key'])


def upload_file(file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        response = s3.upload_file(file_name, BucketName, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

