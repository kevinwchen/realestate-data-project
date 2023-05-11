import requests
import json
import time
from api_variables import api_host, headers

url = 'https://' + api_host + "/properties/list"

# Set property query parameters
channel = "rent"
searchLocation = "Chatswood, NSW 2067"
searchLocationSubtext = "Suburb"
type = "suburb"
pageSize = 30 # max is 30

queryParams = {"channel":channel,
               "searchLocation":searchLocation,
               "searchLocationSubtext":searchLocationSubtext,
               "type":type,
               "page":"1",
               "pageSize":pageSize,
               "sortType":"relevance",
               "surroundingSuburbs":"true",
               "ex-under-contract":"false"}


test_response = requests.get(url, headers=headers, params=queryParams)


if test_response.status_code == 200:
    # Get number of pages to iterate through
    test_data = test_response.json()
    totalResults = test_data['totalResultsCount']
    totalPages = int(totalResults/pageSize)
    if totalResults % pageSize != 0: totalPages += 1

    # Get data
    allResultsData = []
    for page in range(1, totalPages + 1):
        print(f"Processing page {page}...")
        queryParams = {"channel":channel,
               "searchLocation":searchLocation,
               "searchLocationSubtext":searchLocationSubtext,
               "type":type,
               "page":page,
               "pageSize":pageSize,
               "sortType":"relevance",
               "surroundingSuburbs":"true",
            #    "minimumBedrooms":"1",
            #    "maximumBedrooms":"10",
            #    "minimumBathroom":"1",
            #    "minimumCars":"1",
            #    "minimumPrice":"0",
            #    "maximumPrice":"10",
               "ex-under-contract":"false"}
        response = requests.get(url, headers=headers, params=queryParams)

        if response.status_code == 200:
            pageData = response.json()
            tieredResults = pageData['tieredResults']
            for i in range(len(tieredResults)):
                for j in range(len(tieredResults[i]['results'])):
                    propertyData = tieredResults[i]['results'][j]
                    allResultsData.append(tieredResults[i]['results'][j])
        else:
            print(f"Error: {test_response.status_code}")
        time.sleep(1)

    print(f"Total properties: {len(allResultsData)}")
    with open("properties.json", "w") as output:
        output.write(json.dumps(allResultsData))
else:
    print(f"Error: {test_response.status_code}")