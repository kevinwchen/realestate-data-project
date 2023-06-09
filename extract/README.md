# Extract

## 1. Extract from API

Real estate listings are extracted from the realty-in-au.p.rapidapi.com API endpoint. The suburb/region details can be queried first using the **api_auto_complete.py** script. A suburb/region can be selected from the response to be entered into the **api_get_properties.py** query parameters. The list of properties from the query will be saved to **outputs/properties.json**.

## 2. MinIO

Start the MinIO server in the download directory using (for Windows):

```ps
.\minio.exe server c:\minio --console-address :9090
```

Upload the extracted data to your S3 bucket using **file_uploader.py**.
