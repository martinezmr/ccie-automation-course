from getpass import getpass

import requests
import urllib3

# Disable SSL warnings for demo purposes (not recommended for production)
urllib3.disable_warnings()

# Prompt user for APIC details, with defaults for convenience
hostname = (
    input("IP address or hostname: ") or "https://apic.sandbox.ccie-automation.com/api"
)
username = input("Username: ") or "admin"
password = getpass() or "HZ536cHZcM9"

# Construct the base URL for API requests
base_url = f"https://{hostname}/api"

# --- Step 1: Authenticate with APIC ---

# Define the authentication endpoint
path = "/aaaLogin.json"
url = f"{base_url}{path}"

# Prepare the authentication payload as per APIC API requirements
auth_payload = {
    "aaaUser": {
        "attributes": {
            "name": username,
            "pwd": password,
        }
    }
}

# Show what will be sent to the server
print(f"➡️ Sending POST request to {url}")
print(f"  with payload: {auth_payload}")

# Send the authentication request using HTTP POST
rsp = requests.post(
    url,
    json=auth_payload,
    verify=False,  # Ignore SSL certificate validation (for demo)
)

# Parse the JSON response from APIC
auth_data = rsp.json()
print(
    f"⬅️ Received a {type(auth_data)} response and HTTP status code {rsp.status_code}"
)

# Extract the authentication token from the response
token = auth_data["imdata"][0]["aaaLogin"]["attributes"]["token"]
# Prepare cookies for subsequent authenticated requests
apic_cookies = {"APIC-Cookie": token}

# --- Step 2: Create a new tenant ---

# Define the endpoint for tenant creation
path = "/mo/uni/tn-Automation-Test.json"
url = f"{base_url}{path}"

# Prepare the payload to create a tenant named "Automation-Test"
tenant_payload = {
    "fvTenant": {
        "attributes": {
            "name": "Automation-Test",
        }
    }
}

# Show what will be sent to the server for tenant creation
print(f"➡️ Sending POST request to {url}")
print(f"  with cookies: {apic_cookies}")
print(f"  with payload: {tenant_payload}")

# Send the tenant creation request using HTTP POST, including authentication cookies
rsp = requests.post(
    url,
    cookies=apic_cookies,
    json=tenant_payload,
    verify=False,
)
# Print the HTTP status code and reason to confirm success or failure
print(f"⬅️ Received HTTP status code {rsp.status_code} / {rsp.reason}")
