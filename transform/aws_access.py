# Add imports
import os
from dotenv import load_dotenv
load_dotenv()

# S3 bucket details
access_key = os.getenv('AWS-ACCESS-KEY')
secret_key = os.getenv('AWS-SECRET-KEY')
bucket_name = os.getenv('AWS-BUCKET-NAME')