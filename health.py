import requests

headers = {
    "Authorization": "6YQG2CLWRFG7WVHXLLVEDBB0U9P8PJUEN5SLGFEP",
    "accept": "application/json",
    "content-type": "application/json"
}
response = requests.get("https://api.runpod.ai/v2/bgc1bptbd1dnqs/health", headers=headers)
print(response.status_code)
print(response.text)