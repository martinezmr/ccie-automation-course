import meraki
# import logging

class MerakiProvisioningClient:
    def __init__(self, api_key, org_id):
        self.org_id = org_id
        # The library handles 429 (rate limit) retries automatically
        self.dashboard = meraki.DashboardAPI(
            api_key,
            base_url='https://api.meraki.com/api/v1/',
            print_console=False,
            suppress_logging=True
        )

    def create_branch_network(self, name, product_types=['appliance', 'switch', 'wireless']):
        """Creates a new combined network for a branch."""
        try:
            network = self.dashboard.organizations.createOrganizationNetwork(
                self.org_id,
                name=name,
                productTypes=product_types,
                timeZone='America/Chicago' # Match your pilot region
            )
            print(f"Successfully created network: {name} (ID: {network['id']})")
            return network['id']
        except meraki.APIError as e:
            print(f"Error creating network {name}: {e}")
            return None

    def bind_to_template(self, network_id, template_id, auto_bind=True):
        """Binds a network to a configuration template."""
        try:
            self.dashboard.networks.bindNetwork(
                network_id, 
                configTemplateId=template_id, 
                autoBind=auto_bind
            )
            print(f"Network {network_id} bound to template {template_id}")
        except meraki.APIError as e:
            print(f"Error binding network: {e}")

    def claim_devices_to_network(self, network_id, serials):
        """Claims a list of serial numbers into a specific network."""
        try:
            self.dashboard.networks.claimNetworkDevices(
                network_id, 
                serials=serials
            )
            print(f"Claimed {len(serials)} devices to network {network_id}")
        except meraki.APIError as e:
            print(f"Error claiming devices: {e}")

    def get_template_id_by_name(self, template_name):
        """Helper to find a template ID using its display name."""
        templates = self.dashboard.organizations.getOrganizationConfigTemplates(self.org_id)
        for t in templates:
            if t['name'] == template_name:
                return t['id']
        return None

# --- Example Usage for your July Pilot ---
if __name__ == "__main__":
    API_KEY = "your_api_key_here"
    ORG_ID = "your_org_id_here"
    TEMPLATE_NAME = "Standard_Branch_Template"

    client = MerakiProvisioningClient(API_KEY, ORG_ID)
    
    # 1. Find your Golden Template
    target_template_id = client.get_template_id_by_name(TEMPLATE_NAME)

    # 2. Define your Pilot Sites
    pilot_sites = {
        "Pilot-Branch-01": ["XXXX-XXXX-XXXX", "YYYY-YYYY-YYYY"], # MX and MS serials
        "Pilot-Branch-02": ["ZZZZ-ZZZZ-ZZZZ", "AAAA-AAAA-AAAA"]
    }

    # 3. Execution Loop
    for site_name, serials in pilot_sites.items():
        net_id = client.create_branch_network(site_name)
        if net_id:
            client.bind_to_template(net_id, target_template_id)
            client.claim_devices_to_network(net_id, serials)