"""
OAuth2 utilities

License:
Copyright © 2017 The Climate Corporation
"""

from base64 import b64encode
from urllib.parse import urlencode

import requests

def authorization_header(client_id, client_secret):
    pair = '{}:{}'.format(client_id, client_secret)
    encoded = b64encode(pair.encode('ascii')).decode('ascii')
    return 'Basic {}'.format(encoded)

def authorization_data(code, redirect):
    params = {
        'grant_type':   'authorization_code',
        'redirect_uri': redirect,
        'code':         code
    }
    return urlencode(params)

def request(uri, code, client_id, client_secret, redirect):
    headers = {
        'authorization': authorization_header(client_id, client_secret),
        'content-type':  'application/x-www-form-urlencoded',
        'accept':        'application/json'
    }
    data = authorization_data(code, redirect)

    res = requests.post(uri, headers=headers, data=data)
    if res.status_code == 200:
        return res.json()
