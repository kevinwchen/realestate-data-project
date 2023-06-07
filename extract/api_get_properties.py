import os
import requests
import json
import time
from api_variables import api_host, headers

def main():
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
                    allResultsData = []
                    for j in range(len(tieredResults[i]['results'])):
                        propertyData = tieredResults[i]['results'][j]
                        del propertyData["address"]["postCode"] # remove duplicate key
                        allResultsData.append(tieredResults[i]['results'][j])
                    
                    with open(os.path.join(os.path.dirname(__file__), "outputs", "raw", "properties_" + str(page) + ".json"), "w") as output:
                        output.write(json.dumps(allResultsData,indent=4)) # Write to file for every page processed
            else:
                print(f"Error: {test_response.status_code}")

        print(f"Total properties: {totalResults}")
    else:
        print(f"Error: {test_response.status_code}")

if __name__ == "__main__":
    try:
        main()
    except all:
        print("Error occurred.")
    else:
        print("Data successfully processed.")