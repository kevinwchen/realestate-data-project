import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('X-RAPIDAPI-KEY')
api_host = os.getenv('X-RAPIAPI-HOST')

headers = {
	"X-RapidAPI-Key": api_key,
	"X-RapidAPI-Host": api_host
}