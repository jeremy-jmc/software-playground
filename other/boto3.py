# https://replicate.com/vaibhavs10/incredibly-fast-whisper?prediction=4hbuid3bzbzuarnkxnr6anwyi4&output=json&input=python
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
# https://docs.aws.amazon.com/code-library/latest/ug/python_3_code_examples.html

"""
aws configure
aws sts get-caller-identity
aws s3 ls
"""

import json
import logging
from botocore.exceptions import ClientError
import boto3
import replicate
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


def custom_serializer(obj):
    """Serialize datetime objects to string."""
    if isinstance(obj, datetime):
        return obj.isoformat()


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

# -----------------------------------------------------------------------------
# AWS S3
# -----------------------------------------------------------------------------


s3 = boto3.client('s3')
response = s3.list_buckets()

print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'- {bucket["Name"]}')

bucket_name = "tnknbucket"
print(json.dumps(s3.list_objects(Bucket=bucket_name),
                 default=custom_serializer,
                 indent=2))

presigned_url = create_presigned_url(bucket_name, "audio/recorded_audio.wav")
print(presigned_url)

# -----------------------------------------------------------------------------
# Replicate Incredibly Fast Whisper: Transcribe from presigned URL
# -----------------------------------------------------------------------------

output = replicate.run(
    "vaibhavs10/incredibly-fast-whisper:3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
    input={
        "task": "transcribe",
        "audio": presigned_url,
        "language": "None",
        "timestamp": "chunk",
        "batch_size": 64,
        "diarise_audio": False
    }
)

print(json.dumps(output, indent=2, ensure_ascii=False))
