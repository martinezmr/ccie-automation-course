import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint

BASE_URL = "https://ise.sandbox.ccie-automation.com"
USERNAME = "admin"
PASSWORD = "HZ536cHZcM9"

path = "/api/v1/endpoint"
url = BASE_URL + path
auth = HTTPBasicAuth(USERNAME, PASSWORD)
ise_headers = {"Accept": "application/json"}

response = requests.get(url, auth=auth, headers=ise_headers, verify=False)

pprint(response.json())
