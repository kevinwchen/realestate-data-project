import json
import os
import boto3
from aws_access import bucket_name

# Configure AWS CLI before running this

def main():
    s3 = boto3.resource("s3")

    my_bucket = s3.Bucket(bucket_name)

    for object_summary in my_bucket.objects.filter(Prefix="raw/"):
        obj = s3.Object(bucket_name, object_summary.key)
        file_content = obj.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        for content in json_content:
            displayPrice = content["price"]["display"]
            if hasNum(displayPrice):
                print(displayPrice)

def hasNum(inputString):
    return any(char.isdigit() for char in inputString)

if __name__ == "__main__":
    try:
        main()
    except all:
        print("Error occurred.")