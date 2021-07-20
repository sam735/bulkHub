import boto3
from constant import AWSAccessKeyId,AWSSecretKey

def upload_to_aws(file_obj, bucket_name, s3_file):

    s3 = boto3.client('s3','ap-south-1', aws_access_key_id=AWSAccessKeyId,
                      aws_secret_access_key=AWSSecretKey,
                      verify=False,
                    )

    try :
        upload_details = s3.upload_fileobj(file_obj, bucket_name, s3_file,ExtraArgs={
                            "ACL": 'public-read',
                            "ContentDisposition" : 'inline',
                            "ContentType": "image/jpeg"
                        })
        return True
    except Exception as e:
        return False