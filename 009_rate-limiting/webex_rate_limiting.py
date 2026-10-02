from datetime import datetime, timezone
from getpass import getpass
from time import sleep

import requests

# Prompt user for their Webex Personal Access Token (PAT) securely.
# If no input is given, use a default token (for demo purposes).
pat = getpass("Personal Access Token: ")

# Ask user for the email address to monitor messages from.
# If no input is given, use a default email.
sender = input("Monitor messages from: ")

# Define the base URL and endpoint path for the Webex REST API.
base_url = "https://webexapis.com/v1"
path = "/messages/direct"
url = f"{base_url}{path}"

# Set up HTTP headers for the REST API request.
# Include the PAT for authorization.
webex_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {pat}",
}

print(f"👀 Checking new messages from {sender}")

# Track the time after which new messages should be announced.
announce_message_after = datetime.now(timezone.utc)

# Main loop to continuously check for new messages.
while True:
    # Send a GET request to the Webex API to fetch direct messages from the specified sender.
    rsp = requests.get(
        url,
        headers=webex_headers,
        params={"personEmail": sender},
    )

    # Handle rate limiting (HTTP 429 status code).
    # If rate limited, wait for the specified time before retrying.
    if rsp.status_code == 429:
        retry_after = rsp.headers.get("Retry-After")
        print(f"🛑 Rate limited - waiting for {retry_after} seconds.")
        sleep(int(retry_after))
    else:
        # Parse the JSON response and get the latest message.
        latest_message = rsp.json()["items"][0]
        # Convert the message creation time to a datetime object.
        latest_message_time = datetime.fromisoformat(latest_message["created"])

        # If the latest message is newer than the last announced message, print it.
        if latest_message_time > announce_message_after:
            print("✉️ New message received:")
            print(latest_message["text"])
            announce_message_after = latest_message_time
