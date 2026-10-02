"""
Webhook service for logging events.
https://webhook.site/#!/view/2e979893-5f1b-49ea-acf3-41ae70eeccb0

Let's you test and debug webhooks by sending HTTP requests
to a unique URL and viewing the results in real-time.
"""

import requests
import json
from datetime import datetime, timezone

event_happened_at = datetime.now(timezone.utc).isoformat()

webhook_url = "https://webhook.site/2e979893-5f1b-49ea-acf3-41ae70eeccb0"

payload = {
    "type": "exam.result",
    "timestamp": event_happened_at,
    "data": {"exams": [{"name": "AUTOCOR", "exam": "350-901", "result": "PASS"}]},
}

serialized_payload = json.dumps(payload)

requests.post(webhook_url, data=serialized_payload)
