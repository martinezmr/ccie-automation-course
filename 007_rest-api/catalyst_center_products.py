import requests
import urllib3
from pprint import pprint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://catalyst-center.sandbox.ccie-automation.com"
username = "admin"
password = "HZ536cHZcM9"

token_endpoint = "/dna/system/api/v1/auth/token"

url = base_url + token_endpoint

headers = {"Content-Type": "application/json", "Accept": "application/json"}

response = requests.post(url, auth=(username, password), headers=headers, verify=False)
token = response.json()["Token"]

headers["X-Auth-Token"] = token

endpoint = "/dna/intent/api/v1/productNames"

url = base_url + endpoint

response = requests.get(url, headers=headers, verify=False)

pprint(response.json())
