import os
import requests
import json
from api_variables import api_host, headers


url = 'https://' + api_host + "/auto-complete"

query = input('Enter a search query: ')
queryParams = {"query": query}

response = requests.get(url, headers=headers, params=queryParams)

if response.status_code == 200:
    print(response.json())
    with open(os.path.join(os.path.dirname(__file__), "outputs", "auto_complete.json"), "w") as output:
        json.dump(response.json(), output)
else:
    print(f"Error: {response.status_code}")