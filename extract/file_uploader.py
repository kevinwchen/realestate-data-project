from minio import Minio
from minio.error import S3Error
import os
from dotenv import load_dotenv

load_dotenv()

aws_key = os.getenv('AWS-ACCESS-KEY')
aws_secret = os.getenv('AWS-SECRET-KEY')
aws_bucket_name = os.getenv('AWS-BUCKET-NAME')

def main():
    # Create a client with the MinIO server playground, its access key and secret key.
    client = Minio(
        "s3.amazonaws.com", access_key=aws_key, secret_key=aws_secret,
    )

    # Make bucket if not existing
    found = client.bucket_exists(aws_bucket_name)
    if not found:
        client.make_bucket(aws_bucket_name)
    else:
        print(f"Bucket '{aws_bucket_name}' already exists")

    # Upload data
    directory =  os.path.join(os.path.dirname(__file__), "outputs", "raw")
    for fname in os.scandir(directory):
        print(f"Uploading {fname.name}")
        client.fput_object(aws_bucket_name, "raw/" + fname.name, os.path.join(directory, fname.name))
    print(f"Data uploaded to bucket {aws_bucket_name}")

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)