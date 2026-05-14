import requests
import time
from constants import MERAKI_API_KEY, MERAKI_BASE_URL
from pprint import pprint

class MerakiRequestsClient:
    def __init__(self):
        self.base_url = MERAKI_BASE_URL
        self.headers = {
            "X-Cisco-Meraki-API-Key": MERAKI_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.org_id = self.get_org_id()


    def _make_request(self, method, endpoint, data=None):
        """Internal helper to handle requests and basic rate limiting."""
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data)
        
        # Meraki uses 429 for rate limiting. 
        # Basic retry logic for a 1-second backoff.
        if response.status_code == 429:
            time.sleep(1)
            return self._make_request(method, endpoint, data)
            
        if not response.ok:
            print(f"Error {response.status_code}: {response.text}")
            return None
            
        return response.json()

    def create_branch_network(self, name, product_types=['appliance', 'switch', 'wireless']):
        """Creates a combined network for a branch."""
        endpoint = f"/organizations/{self.org_id}/networks"
        payload = {
            "name": name,
            "productTypes": product_types,
            "timeZone": "America/Chicago"
        }
        return self._make_request("POST", endpoint, payload)

    def bind_to_template(self, network_id, template_id, auto_bind=True):
        """Binds a network to a configuration template."""
        endpoint = f"/networks/{network_id}/bind"
        payload = {
            "configTemplateId": template_id,
            "autoBind": auto_bind
        }
        return self._make_request("POST", endpoint, payload)

    def claim_devices(self, network_id, serials):
        """Claims serial numbers into a network."""
        endpoint = f"/networks/{network_id}/devices/claim"
        payload = {"serials": serials}
        return self._make_request("POST", endpoint, payload)

    def get_template_id(self, name):
        """Finds a template ID by its name."""
        endpoint = f"/organizations/{self.org_id}/configTemplates"
        templates = self._make_request("GET", endpoint)
        if templates:
            for t in templates:
                if t['name'] == name:
                    return t['id']
        return None
    
    def get_org_id(self):
        """Returns the organization ID."""
        endpoint = "/organizations"
        org_id = self._make_request("GET", endpoint)
        if org_id:
            return org_id[0]["id"]
        else:
            raise Exception(
                "Unable to retrieve organization ID. Check your API key and permissions."
            )
        # return self.org_id

def provision_site():
    client = MerakiRequestsClient()
    
    # 1. Get Template
    template_id = client.get_template_id("Standard_Branch_Template")
    
    # 2. Provision Site
    if template_id:
        new_net = client.create_branch_network("Pilot-Branch-Requests-01")
        if new_net:
            net_id = new_net['id']
            client.bind_to_template(net_id, template_id)
            client.claim_devices(net_id, ["XXXX-XXXX-XXXX"])

def main():
    client = MerakiRequestsClient()
    response = client.get_org_id()
    pprint(response[0]["id"])

# --- Usage Example ---
if __name__ == "__main__":
    main()