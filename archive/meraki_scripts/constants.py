import os
from dotenv import load_dotenv

load_dotenv()

MERAKI_BASE_URL = "https://api.meraki.com/api/v1"
MERAKI_API_KEY = os.getenv("MERAKI_API_KEY")
