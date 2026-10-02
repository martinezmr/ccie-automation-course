import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timezone

import requests

# All webhooks are generated based on events. Knowing the exact time of the event in important.
event_happened_at = datetime.now(timezone.utc)

# From the time of the event happening and until the webhook is actually sent, time may pass
webhook_processed_at = datetime.now(timezone.utc)


payload = {
    "type": "ccnp.automation",
    "timestamp": event_happened_at.isoformat(),
    "data": {
        "courses": [
            {
                "name": "AUTOCOR",
                "exam": "350-901",
            },
        ]
    },
}

# Convert the payload object into a string that we can send as the HTTP body.
serialized_payload = json.dumps(payload)

# Generate a message ID and prepend with msg_
random_string = secrets.token_urlsafe()
message_id = f"msg_{random_string}"

# Convert the webhook processing timestamp into a POSIX integer
# this is a standard timestamp mechanism based on counting the number of seconds
# since January 1st 1970 00:00 UTC
signing_timestamp = int(webhook_processed_at.timestamp())

# To ensure authenticity of the webhook, it needs to be signing.
# A combined string consisting of the message ID, timestamp and payload
# will be used for signing.
signing_content = f"{message_id}.{signing_timestamp}.{serialized_payload}"

# The sender ("producer") and receiver ("consumer") needs to agree on a base64 encoded signing secret.
# It is prepended with whsec_ to indicate that it is a symetric webhook secret.
# But this prefix of 6 characters needs to be stripped, and the base64 decoded to a byte stream before actually calculating the signature.
signing_secret = "whsec_1fmy1Z7mFFyp5m01zZMYMKfilFBrXyzB"
secret_key = base64.b64decode(signing_secret[6:])

# The hmac module combines the decoded byte stream of the signing secret with the content and calcuates a SHA256 checksum
signature_bytes = hmac.new(secret_key, signing_content.encode("utf-8"), hashlib.sha256)

# Convert the calculated value to hex values represented with utf-8, and prepend with v1,
signature = f"v1,{base64.b64encode(signature_bytes.digest()).decode('utf-8')}"

# Construct the webhook headers
headers = {
    "webhook-id": message_id,
    "webhook-timestamp": signing_timestamp,
    "webhook-signature": signature,
}

# Send the webhook
requests.post(
    "https://webhook.site/0456ef91-7c29-4eb0-b309-c7ecc0f3650e",
    headers=headers,
    data=serialized_payload,
)