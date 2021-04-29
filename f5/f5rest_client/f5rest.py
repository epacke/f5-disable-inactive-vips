import requests, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class F5rest:
    def __init__(self, username, password, device, verify_ssl=True):
        self.device = device
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self._token = None

    @property
    def token(self):
        if not self._token:
            body = {
                'username': self.username,
                'password': self.password,
                'loginProviderName': 'tmos'
            }

            token_response = requests.post(
                f'https://{self.device}/mgmt/shared/authn/login',
                verify=self.verify_ssl,
                auth=(self.username, self.password), json=body) \
                .json()

            self._token = token_response['token']['token']
        return self._token

    def get_endpoint(self, endpoint):
        headers = {
            'X-F5-Auth-Token': self.token
        }

        return requests.get(f'https://{self.device}{endpoint}', headers=headers, verify=self.verify_ssl).json()

    def patch_endpoint(self, endpoint, body):
        headers = {
            'X-F5-Auth-Token': self.token,
        }

        return requests.patch(f'https://{self.device}{endpoint}', json=body, headers=headers, verify=self.verify_ssl).json()

    def get_virtual_server_stats(self):
        response = self.get_endpoint('/mgmt/tm/ltm/virtual/stats')
        return response

    def disable_virtual_server(self, name, comment):
         self.patch_endpoint(f'/mgmt/tm/ltm/virtual/{name}', {
            'disabled': True,
            'description': comment
        })