"""
Climate API demo code. This module shows how to:

- Log in with Climate
- Refresh the access_token
- Fetch growing seasons
- Fetch harvest reports

License:
Copyright © 2022 Climate, LLC
"""

import requests

import os
import json
from base64 import b64encode
from urllib.parse import urlencode
from curlify import to_curl
from logger import Logger


json_content_type = 'application/json'

base_login_uri = 'https://climate.com/static/app-login/index.html'
token_uri = 'https://api.climate.com/api/oauth/token'
api_uri = 'https://platform.climate.com'


def login_uri(client_id, scopes, redirect_uri):
    """
    Builds the URI for 'Log In with FieldView' link.
    The redirect_uri is a uri on your system (this app) that will handle the
    authorization once the user has authenticated with FieldView.
    """
    params = {
        'scope': scopes,
        'page': 'oidcauthn',
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


def authorize(login_code, client_id, client_secret, redirect_uri):
    """
    Exchanges the login code provided on the redirect request for an
    access_token and refresh_token. Also gets user data.
    :param login_code: Authorization code returned from Log In with FieldView
        on redirect uri.
    :param client_id: Provided by Climate.
    :param client_secret: Provided by Climate.
    :param redirect_uri: Uri to your redirect page. Needs to be the same as
        the redirect uri provided in the initial Log In with FieldView request.
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
    Logger().info(to_curl(res.request))
    if res.status_code == 200:
        return res.json()

    Logger().error("Auth failed: %s" % res.status_code)
    Logger().error("Auth failed: %s" % res.json())
    return None


def reauthorize(refresh_token, client_id, client_secret):
    """
    Access_tokens expire after 4 hours. At any point before the end of that
    period you may request a new access_token (and refresh_token) by submitting
    a POST request to the /api/oauth/token end-point. Note that the data
    submitted is slightly different than on initial authorization. Refresh
    tokens are good for 30 days from their date of issue. Once this end-point
    is called, the refresh token that is passed to this call is immediately set
    to expired one hour from "now" and the newly issues refresh token will
    expire 30 days from "now". Make sure to store the new refresh token so you
    can use it in the future to get a new auth tokens as needed. If you lose
    the refresh token there is no effective way to retrieve a new refresh token
    without having the user log in again.
    :param refresh_token: refresh_token supplied by initial
        (or subsequent refresh) call.
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
    Logger().info(to_curl(res.request))
    if res.status_code == 200:
        return res.json()

    log_http_error(res)
    return None


def bearer_token(token):
    """
    Returns content of authorization header to be provided on all non-auth
    API calls.
    :param token: access_token returned from authorization call.
    :return: Formatted header.
    """
    return 'Bearer {}'.format(token)


def log_http_error(response):
    """
    Private function to log errors on server console
    :param response: http response object.
    """
    if response.status_code == 403:
        Logger().error("Permission error, current scopes are - {}".format(
            os.environ['CLIMATE_API_SCOPES']))
    elif response.status_code == 400:
        Logger().error("Bad request - {}".format(response.text))
    elif response.status_code == 401:
        Logger().error("Unauthorized - {}".format(response.text))
    elif response.status_code == 404:
        Logger().error("Resource not found - {}".format(response.text))
    elif response.status_code == 416:
        Logger().error("Range Not Satisfiable - {}".format(response.text))
    elif response.status_code == 500:
        Logger().error("Internal server error - {}".format(response.text))
    elif response.status_code == 503:
        Logger().error("Server busy - {}".format(response.text))


def growingSeasons(field_id, token, api_key):
    """
    Retrieve the growing seasons from Climate. 
    :param field_id: UUID of field to retrieve.
    :param token: access_token
    :param api_key: Provided by Climate
    :return: JSON object with a contentId which is the growingSeasonsContentId
    """
    uri = '{}/v5/growingSeasons'.format(api_uri)
    headers = {
        'authorization': bearer_token(token),
        'x-api-key': api_key
    }
    data = {
        'fieldId': field_id
    }

    res = requests.post(uri, headers=headers, json=data)
    Logger().info(to_curl(res.request))

    if res.status_code == 202:
        return res.json()['contentId']
    log_http_error(res)
    return False


def growingSeasonsContents(content_id, token, api_key):
    """
    Retrieve the growing seasons contents from Climate. 
    :param content_id: UUID of growingSeasonsContentsId to retrieve.
    :param token: access_token
    :param api_key: Provided by Climate
    :return: JSON object with a list of UUID of the growingSeasonsId and year
    """
    uri = '{}/v5/growingSeasonsContents/{}'.format(api_uri, content_id)
    headers = {
        'authorization': bearer_token(token),
        'x-api-key': api_key
    }
    res = requests.get(uri, headers=headers)
    Logger().info(to_curl(res.request))

    if res.status_code == 200:
        pretty_json = json.loads(res.text)
        return json.dumps(pretty_json, indent=4, sort_keys=True)
    log_http_error(res)
    return False


def harvestReports(field_id, seasons, token, api_key):
    """
    Retrieve the harvest reports from Climate. 
    :param field_id: UUID of field to retrieve.
    :param seasons: UUID of growingSeasonsId to retrieve.
    :param token: access_token
    :param api_key: Provided by Climate
    :return: JSON object with a harvest report id
    """
    uri = '{}/v5/harvestReports'.format(api_uri)
    headers = {
        'authorization': bearer_token(token),
        'x-api-key': api_key
    }
    data = {
        'fieldId': field_id,
        'growingSeasons': seasons
    }

    res = requests.post(uri, headers=headers, json=data)
    Logger().info(to_curl(res.request))

    if res.status_code == 202:
        return res.json()['id']
    log_http_error(res)
    return False


def harvestReportsContents(report_id, token, api_key):
    """
    Retrieve the harvest reports contents from Climate. 
    :param report_id: UUID of harvest report id to retrieve.
    :param token: access_token
    :param api_key: Provided by Climate
    :return: JSON object with a list harvest reports
    """
    uri = '{}/v5/harvestReportsContents/{}'.format(api_uri, report_id)
    headers = {
        'authorization': bearer_token(token),
        'x-api-key': api_key
    }
    res = requests.get(uri, headers=headers)
    Logger().info(to_curl(res.request))

    if res.status_code == 200:
        pretty_json = json.loads(res.text)
        return json.dumps(pretty_json, indent=4, sort_keys=True)
    log_http_error(res)
    return False
