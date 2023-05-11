import requests
import json
from api_variables import api_host, headers


url = 'https://' + api_host + "/auto-complete"

query = input('Enter a search query: ')
query_object = {"query": query}

response = requests.get(url, headers=headers, params=query_object)

print(response.json())
with open("auto_complete_out.json", "w") as output:
    json.dump(response.json(), output)