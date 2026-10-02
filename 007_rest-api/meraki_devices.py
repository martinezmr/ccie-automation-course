from getpass import getpass

import requests

# Prompt the user for their Meraki API key securely (input hidden)
apikey = getpass("API key: ")
# Prompt the user for the organization name
org_name = input("Organization name: ")

# --- Step 1: Get organization information ---

# Define the base URL for Meraki's REST API
base_url = "https://api.meraki.com/api/v1"
# Set the API endpoint path for organizations
path = "/organizations"
# Construct the full URL for the GET request
url = f"{base_url}{path}"

# Prepare the HTTP headers required by the Meraki API
meraki_headers = {
    "Content-Type": "application/json",  # Specify the content type
    "Accept": "application/json",  # Specify the accepted response format
    "Authorization": f"Bearer {apikey}",  # Pass the API key as a Bearer token
}

# Print information about the outgoing request for learning purposes
print(f"➡️ Sending GET request to {url}")
print(f"  with headers: {meraki_headers}")

# Send the GET request to retrieve organizations
rsp = requests.get(url, headers=meraki_headers)
# Parse the JSON response into a Python object (usually a list)
organizations = rsp.json()
print(
    f"⬅️ Received a {type(organizations)} response and HTTP status code {rsp.status_code}"
)
# Loop through the organizations to find the one matching the user's input
for org in organizations:
    if org["name"] == org_name:
        print(f"🧪 {org_name} organization found with id {org['id']}")
        organizationId = org["id"]

# --- Step 2: Get devices for the selected organization ---

# Set the API endpoint path for devices in the organization
path = f"/organizations/{organizationId}/devices"
# Construct the full URL for the GET request
url = f"{base_url}{path}"

# Print information about the outgoing request for learning purposes
print(f"➡️ Sending GET request to {url}")
print(f"  with headers: {meraki_headers}")

# Send the GET request to retrieve devices in the organization
rsp = requests.get(
    url,
    headers=meraki_headers,
)

# Parse the JSON response into a Python object (usually a list)
devices = rsp.json()
print(f"⬅️ Received a {type(devices)} response and HTTP status code {rsp.status_code}")

# Access the first device in the list and print its serial number
first_device = devices[0]
print(f"✅ First device serial number: {first_device['serial']}")
