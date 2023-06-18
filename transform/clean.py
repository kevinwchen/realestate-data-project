import boto3
from aws_access import bucket_name
import json
import re
import pandas as pd

# Configure AWS CLI before running this

def main():
    s3 = boto3.resource("s3")
    my_bucket = s3.Bucket(bucket_name)

    df_cols = [
        "type", # rent or buy
        "property_type", # type of propety building
        "address_street", # street address
        "address_suburb", # suburb
        "address_postcode", # postcode
        "address_state", # state
        "price", # price
        "bed", # number of bedrooms
        "bath", # number of bathrooms
        "car", # number of car parking spaces
        ]
    df_listings = pd.DataFrame(columns=df_cols)

    for object_summary in my_bucket.objects.filter(Prefix="raw/"):
        obj = s3.Object(bucket_name, object_summary.key)
        file_content = obj.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        for content in json_content:
            # Check if listing contains price information
            display_price = content["price"]["display"]
            if has_num(display_price):
                display_price = display_price.replace(".00","")
                
                # Remove trailing text after the first space proceeding a digit
                for ichar in range(1, len(display_price)):
                    lastChar = display_price[ichar - 1]
                    char = display_price[ichar]
                    if (char == " " and lastChar.isdigit() == True):
                        price = display_price[0:ichar]
                        break
                price = re.sub("[^0-9]", "", price)
                df = pd.DataFrame({
                    df_cols[0]: [content["channel"]],
                    df_cols[1]: [content["propertyType"]],
                    df_cols[2]: [content["address"]["streetAddress"]],
                    df_cols[3]: [content["address"]["suburb"]],
                    df_cols[4]: [content["address"]["postcode"]],
                    df_cols[5]: [content["address"]["state"]],
                    df_cols[6]: [int(price)],
                    df_cols[7]: [content["features"]["general"]["bedrooms"]],
                    df_cols[8]: [content["features"]["general"]["bathrooms"]],
                    df_cols[9]: [content["features"]["general"]["parkingSpaces"]]
                    }, columns=df_cols)
                print(df.to_string())
                # df_listings.append(df)


def has_num(input_string):
    return any(char.isdigit() for char in input_string)

if __name__ == "__main__":
    try:
        main()
    except all:
        print("Error occurred.")