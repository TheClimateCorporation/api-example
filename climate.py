"""
Climate API demo code. This module shows how to:

- Log in with Climate
- Refresh the access_token
- Fetch fields
- Fetch field boundaries
- Upload files

License:
Copyright © 2017 The Climate Corporation
"""

import requests

import file
from base64 import b64encode
from urllib.parse import urlencode
from curlify import to_curl

json_content_type = 'application/json'
binary_content_type = 'application/octet-stream'

base_login_uri = 'https://climate.com/static/app-login/index.html'
token_uri = 'https://api.climate.com/api/oauth/token'
api_uri = 'https://platform.climate.com'


def login_uri(client_id, redirect_uri):
    """
    URI for 'Log In with FieldView' link. The redirect_uri is a uri on your system (this app) that will handle the
    authorization once the user has authenticated with FieldView.
    """
    params = {
        'scope': 'openid+platform+partnerapis',
        'page': 'oidcauthn',
        'mobile': 'true',
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri
    }
    return '{}?{}'.format(base_login_uri, urlencode(params))


def authorization_header(client_id, client_secret):
    """
    Builds the authorization header unique to your company or application.
    :param client_id: Provided by Climate.
    :param client_secret: Provided by Climate.
    :return: Basic authorization header.
    """
    pair = '{}:{}'.format(client_id, client_secret)
    encoded = b64encode(pair.encode('ascii')).decode('ascii')
    return 'Basic {}'.format(encoded)


def authorize(login_code, client_id, client_secret, redirect_uri, logger):
    """
    Exchanges the login code provided on the redirect request for an access_token and refresh_token. Also gets user
    data.
    :param login_code: Authorization code returned from Log In with FieldView on redirect uri.
    :param client_id: Provided by Climate.
    :param client_secret: Provided by Climate.
    :param redirect_uri: Uri to your redirect page. Needs to be the same as the redirect uri provided in the initial
           Log In with FieldView request.
    :return: Object containing user data, access_token and refresh_token.
    """
    headers = {
        'authorization': authorization_header(client_id, client_secret),
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    data = {
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': login_code
    }
    res = requests.post(token_uri, headers=headers, data=urlencode(data))
    logger.info(to_curl(res.request))
    if res.status_code == 200:
        return res.json()
    else:
        logger.error("Auth failed: %s" % res.status_code)
        logger.error("Auth failed: %s" % res.json())


def reauthorize(refresh_token, client_id, client_secret, logger):
    """
    Access_tokens expire after 30 days. At any point before the end of that period you may request a new access_token
    (and refresh_token) by submitting a POST request to the /api/oauth/token end-point. Note that the data submitted
    is slightly different than on initial authorization.
    :param refresh_token: refresh_token supplied on initial (or subsequent refresh) call.
    :param client_id: Provided by Climate.
    :param client_secret: Provided by Climate.
    :return: Object containing user data, access_token and refresh_token.
    """
    headers = {
        'authorization': authorization_header(client_id, client_secret),
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    res = requests.post(token_uri, headers=headers, data=urlencode(data))
    logger.info(to_curl(res.request))
    if res.status_code == 200:
        return res.json()


def bearer_token(token):
    """
    Returns content of authorization header to be provided on all non-auth API calls.
    :param token: access_token returned from authorization call.
    :return: Formatted header.
    """
    return 'Bearer {}'.format(token)


def get_fields(token, api_key, logger, next_token=None):
    """
    Retrieve a user's field list from Climate. Note that fields (like most data) is paginated to support very large
    data sets. If the status code returned is 206 (partial content), then there is more data to get. The x-next-token
    header provides a "marker" that can be used on another request to get the next page of data. Continue fetching
    data until the status is 200. Note that x-next-token is based on date modified, so storing x-next-token can used
    as a method to fetch updates over longer periods of time (though also note that this will not result in fetching
    deleted objects since they no longer appear in lists regardless of their modified date).
    :param token: access_token
    :param api_key: Provided by Climate.
    :param next_token: Pagination token from previous request, or None.
    :return: A (possibly empty) list of fields.
    """
    uri = '{}/v4/fields'.format(api_uri)
    headers = {
        'authorization': bearer_token(token),
        'accept': json_content_type,
        'x-api-key': api_key,
        'x-next-token': next_token
    }

    res = requests.get(uri, headers=headers)
    logger.info(to_curl(res.request))

    if res.status_code == 200:
        return res.json()['results']
    if res.status_code == 206:
        next_token = res.headers['x-next-token']
        return res.json()['results'] + get_fields(token, api_key, logger, next_token)
    else:
        return []


def get_boundary(boundary_id, token, api_key, logger):
    """
    Retrieve field boundary from Climate. Note that boundary objects are immutable, so whenever a field's boundary is
    updated the boundaryId property of the field will change and you will need to fetch the updated boundary.
    :param boundary_id: UUID of field boundary to retrieve.
    :param token: access_token
    :param api_key: Provided by Climate
    :return: geojson object representing the boundary of the field.
    """
    uri = '{}/v4/boundaries/{}'.format(api_uri, boundary_id)
    headers = {
        'authorization': bearer_token(token),
        'accept': json_content_type,
        'x-api-key': api_key
    }

    res = requests.get(uri, headers=headers)
    logger.info(to_curl(res.request))

    if res.status_code == 200:
        return res.json()
    else:
        return None


def upload(f, content_type, token, api_key, logger):
    """Upload a file with the given content type to Climate

    This example supports files up to 5 MiB (5,242,880 bytes).

    Returns True if the upload is successful, False otherwise.
    """
    CHUNK_SIZE = 5 * 1024 * 1024

    uri = '{}/v4/uploads'.format(api_uri)
    headers = {
        'authorization': bearer_token(token),
        'x-api-key': api_key
    }
    md5 = file.md5(f)
    length = file.length(f)
    data = {
        'md5': md5,
        'length': length,
        'contentType': content_type
    }

    # initiate upload
    res = requests.post(uri, headers=headers, json=data)
    logger.info(to_curl(res.request))

    if res.status_code == 201:
        upload_id = res.json()
        logger.info("Upload Id: %s" % upload_id)
        put_uri = '{}/{}'.format(uri, upload_id)

        # for this example, size is assumed to be small enough for a
        # single upload (less than or equal to 5 MiB)
        headers['content-range'] = 'bytes {}-{}/{}'.format(0, (length - 1), length)
        headers['content-type'] = binary_content_type

        f.seek(0)

        # send image
        for position in range(0, length, CHUNK_SIZE):
            buf = f.read(CHUNK_SIZE)
            headers['content-range'] = 'bytes {}-{}/{}'.format(position, position + len(buf) - 1, length)
            try:
                res = requests.put(put_uri, headers=headers, data=buf)
                logger.info(headers)
            except Exception as e:
                logger.error("Exception: %s" % e)

        if res.status_code == 204:
            return upload_id
    return False
