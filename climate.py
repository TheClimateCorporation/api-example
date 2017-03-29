"""
Climate client

- Log in with Climate
- Fetch fields
- Fetch field boundaries
- Upload files

License:
Copyright © 2017 The Climate Corporation
"""

from urllib.parse import urlencode

import requests

import file
import oauth2

json_content_type = 'application/json'
binary_content_type = 'application/octet-stream'

base_login_uri = 'https://climate.com/static/app-login/index.html'
token_uri = 'https://api.climate.com/api/oauth/token'
api_uri = 'https://platform.climate.com'

def login_uri(client_id, redirect_uri):
    """URI for 'Log in with Climate' redirect"""
    params = {
        'scope':         'openid+platform+partnerapis',
        'page':          'oidcauthn',
        'mobile':        'true',
        'response_type': 'code',
        'client_id':     client_id,
        'redirect_uri':  redirect_uri
    }
    return '{}?{}'.format(base_login_uri, urlencode(params))

def authenticate(login_code, client_id, client_secret, redirect_uri):
    """Authenticate with Climate"""
    return oauth2.request(token_uri,
                          code=login_code,
                          client_id=client_id,
                          client_secret=client_secret,
                          redirect=redirect_uri)

def bearer_token(token):
    return 'Bearer {}'.format(token)

def get_fields(token, api_key, next_token=None):
    """Retrieve a user's field list from Climate"""
    uri = '{}/v4/fields'.format(api_uri)
    headers = {
        'authorization': bearer_token(token),
        'accept':        json_content_type,
        'x-api-key':     api_key,
        'x-next-token':  next_token
    }

    res = requests.get(uri, headers=headers)

    if res.status_code == 200:
        return res.json()['results']
    if res.status_code == 206:
        next_token = res.headers['x-next-token']
        return res.json()['results'] + get_fields(token, api_key, next_token)
    else:
        return []

def get_boundary(boundary_id, token, api_key):
    """Retrieve field boundary from Climate"""
    uri = '{}/v4/boundaries/{}'.format(api_uri, boundary_id)
    headers = {
        'authorization': bearer_token(token),
        'accept':        json_content_type,
        'x-api-key':     api_key
    }

    res = requests.get(uri, headers=headers)

    if res.status_code == 200:
        return res.json()
    else:
        return None

def upload(f, content_type, token, api_key):
    """Upload a file with the given content type to Climate

    This example supports files up to 5 MiB (5,242,880 bytes).

    Returns True if the upload is successful, False otherwise.
    """
    uri = '{}/v4/uploads'.format(api_uri)
    headers = {
        'authorization': bearer_token(token),
        'x-api-key':     api_key
    }
    md5 = file.md5(f)
    length = file.length(f)
    data = {
        'md5':          md5,
        'length':       length,
        'content-type': content_type
    }

    # initiate upload
    res = requests.post(uri, headers=headers, json=data)

    if res.status_code == 201:
        upload_id = res.text[1:-1] # extract from json string
        put_uri = '{}/{}'.format(uri, upload_id)

        # for this example, size is assumed to be small enough for a
        # single upload (less than or equal to 5 MiB)
        headers['content-range'] = 'bytes {}-{}/{}'.format(0, (length - 1), length)
        headers['content-type'] = binary_content_type

        f.seek(0)

        # send image
        res = requests.put(put_uri, headers=headers, data=f)

        if res.status_code == 204:
            return True
    return False
