import json
import os
import boto3
from aws_access import bucket_name

# Configure AWS CLI before running this

s3 = boto3.resource("s3")

my_bucket = s3.Bucket(bucket_name)

for object_summary in my_bucket.objects.filter(Prefix="raw/"):
    print(object_summary.key)

