from minio import Minio
from minio.error import S3Error
import os
from dotenv import load_dotenv

load_dotenv()

aws_key = os.getenv('AWS-ACCESS-KEY')
aws_secret = os.getenv('AWS-SECRET-KEY')

def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "s3.amazonaws.com",
        access_key=aws_key,
        secret_key=aws_secret,
    )
    
    bucket_name = "kevinwchen-bucket-real-estate"

    # Make 'real-estate' bucket if not exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
    else:
        print(f"Bucket '{bucket_name}' already exists")

    # Upload data
    client.fput_object(bucket_name, "properties.json", os.path.join(os.path.dirname(__file__), "output", "properties.json"))
    print(f"Data uploaded to bucket {bucket_name}")

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)