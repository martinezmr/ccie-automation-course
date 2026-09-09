import requests

TOKEN = "NTE2NTBjMWQtYTAxNy00YjI4LWFlOTQtZTdhZDVlOTgwMmVlNGI5ZDU1MmEtNzJh_P0A1_fed4bf80-aec1-4e6e-88d0-c7e1787ad33a"

BASE_URL = "https://webexapis.com"

path = "/v1/messages"

url = BASE_URL + path

webex_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}

webex_payload = {
    "toPersonEmail": "mmartinez1513@gmail.com",
    "text": "This is a test message.",
}

response = requests.post(url=url, headers=webex_headers, json=webex_payload)

print(f"Received HTTP status code: {response.status_code} / {response.reason} / {response.text}")