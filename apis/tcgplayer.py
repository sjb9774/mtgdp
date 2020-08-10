import requests
import json


API_URL = "https://api.tcgplayer.com/"
API_VERSION = "1.39.0"


class TcgPlayerBearerToken:

    def __init__(self, access_token=None, expires_in=None, user_name=None, issued=None, expires=None, **kwargs):
        self.access_token = access_token

    def get_value(self):
        return self.access_token


def send_request(path=None, http_method=None, query_params=None, payload=None, headers=None, versioned=True, debug=False):
    query_params = query_params or {}
    headers = headers or {}
    payload = payload or {}

    if versioned:
        full_path = f"{API_URL}{API_VERSION}/{path.rstrip('/')}"
    else:
        full_path = f"{API_URL}{path.rstrip('/')}"
    if debug:
        print(f'{full_path} - {query_params}')
    response = requests.request(http_method, full_path, headers=headers, data=payload, params=query_params)
    if debug:
        print(json.dumps(response.json()))
    return response.json()


def get_bearer_token(public_key=None, private_key=None):
    token_response = send_request(
        path="token",
        http_method="POST",
        payload={
            "grant_type": "client_credentials",
            "client_id": public_key,
            "client_secret": private_key
        },
        versioned=False
    )
    return TcgPlayerBearerToken(**token_response)
