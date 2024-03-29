"""
Climate API demo code. This module shows how to:

- Log in with Climate
- Refresh the access_token
- Fetch fields
- Fetch field boundaries
- Upload files

License:
Copyright © 2018 The Climate Corporation
"""

import requests

import file
import os
from base64 import b64encode
from urllib.parse import urlencode
from curlify import to_curl
from logger import Logger


json_content_type = 'application/json'
binary_content_type = 'application/octet-stream'
metadata_content_types = ['application/vnd.climate.as-applied.zip']

base_login_uri = 'https://climate.com/static/app-login/index.html'
token_uri = 'https://api.climate.com/api/oauth/token'
api_uri = 'https://platform.climate.com'
CHUNK_SIZE = 5 * 1024 * 1024


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


def get_fields(token, api_key, next_token=None):
    """
    Retrieve a user's field list from Climate. Note that fields
    (like most data) is paginated to support very large
    data sets. If the status code returned is 206 (partial content), then
    there is more data to get. The x-next-token header provides a "marker"
    that can be used on another request to get the next page of data.
    Continue fetching data until the status is 200. Note that x-next-token
    is based on date modified, so storing x-next-token can used as a method
    to fetch updates over longer periods of time (though also note that this
    will not result in fetching deleted objects since they no longer appear in
    lists regardless of their modified date).
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
    Logger().info(to_curl(res.request))

    if res.status_code == 200:
        return res.json()['results']
    if res.status_code == 206:
        next_token = res.headers['x-next-token']
        return res.json()['results'] + get_fields(token, api_key, next_token)

    log_http_error(res)
    return []


def get_boundary(boundary_id, token, api_key):
    """
    Retrieve field boundary from Climate. Note that boundary objects are
    immutable, so whenever a field's boundary is updated the boundaryId
    property of the field will change and you will need to fetch the
    updated boundary.
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
    Logger().info(to_curl(res.request))

    if res.status_code == 200:
        return res.json()

    log_http_error(res)
    return None


def upload(f, content_type, token, api_key):
    """Upload a file with the given content type to Climate

    This example supports files up to 5 MiB (5,242,880 bytes).

    Returns The upload id if the upload is successful, False otherwise.
    """
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

    if any(content_type in ct for ct in metadata_content_types):
        data['metadata'] = {
            'fileName' : f.filename
        }

    # initiate upload
    res = requests.post(uri, headers=headers, json=data)
    Logger().info(to_curl(res.request))

    if res.status_code == 201:
        upload_id = res.json()
        Logger().info("Upload Id: %s" % upload_id)
        put_uri = '{}/{}'.format(uri, upload_id)

        # for this example, size is assumed to be small enough for a
        # single upload (less than or equal to 5 MiB)
        headers['content-range'] = 'bytes {}-{}/{}'.format(0,
                                                           (length - 1),
                                                           length)
        headers['content-type'] = binary_content_type

        f.seek(0)

        # send image
        for position in range(0, length, CHUNK_SIZE):
            buf = f.read(CHUNK_SIZE)
            headers['content-range'] = 'bytes {}-{}/{}'.format(
                position, position + len(buf) - 1, length)
            try:
                res = requests.put(put_uri, headers=headers, data=buf)
                Logger().info(headers)
            except Exception as e:
                Logger().error("Exception: %s" % e)

        if res.status_code == 204:
            return upload_id

    return False


def get_upload_status(upload_id, token, api_key):
    """
    Retrieve the status of an upload. See
    https://dev.fieldview.com/technical-documentation/ for possible status
    values and their meaning.
    :param upload_id: id of upload
    :param token: access_token
    :param api_key: Provided by Climate
    :return: status json object containing upload id and status.
    """
    uri = '{}/v4/uploads/{}/status'.format(api_uri, upload_id)
    headers = {
        'authorization': bearer_token(token),
        'accept': json_content_type,
        'x-api-key': api_key
    }

    res = requests.get(uri, headers=headers)
    Logger().info(to_curl(res.request))

    if res.status_code == 200:
        return res.json()

    log_http_error(res)
    return None


def get_scouting_observations(token,
                              api_key,
                              limit=100,
                              next_token=None,
                              occurred_after=None,
                              occurred_before=None):
    """
    Retrieve a list of scouting observations created or updated by the user
    identified by the Authorization header.
    https://dev.fieldview.com/technical-documentation/ for possible status
    values and their meaning.
    :param token: access_token
    :param api_key: Provided by Climate
    :param next-token: Opaque string which allows for fetching the next batch
        of results.
    :param limit: Max number of results to return per batch. Must be between
        1 and 100 inclusive.
    :param occurred_after: Optional start time by which to filter layer
         results.
    :param occurred_before: Optional end time by which to filter layer results.
    :return: status json object containing scouting observation list
        and status.
    """
    uri = '{}/v4/layers/scoutingObservations'.format(api_uri)
    headers = {
        'authorization': bearer_token(token),
        'accept': json_content_type,
        'x-api-key': api_key,
        'x-limit': str(limit),
        'x-next-token': next_token
    }
    params = {
        'occurredAfter': occurred_after,
        'occurredBefore': occurred_before
    }

    res = requests.get(uri, headers=headers, params=params)
    Logger().info(to_curl(res.request))

    if res.status_code == 200:
        return res.json()['results']
    if res.status_code == 206:
        next_token = res.headers['x-next-token']
        return res.json()['results'] + \
            get_scouting_observations(token,
                                      api_key,
                                      limit,
                                      next_token,
                                      occurred_after,
                                      occurred_before)
    log_http_error(res)
    return []


def get_scouting_observation(token, api_key, scouting_observation_id):
    """
    Retrieve an individual scouting observation by id. Ids are retrieved via
    the /layers/scoutingObservations route.
    https://dev.fieldview.com/technical-documentation/ for possible status
    values and their meaning.
    :param token: access_token
    :param api_key: Provided by Climate
    :param scouting_observation_id: Unique identifier of the
        Scouting Observation.

    """
    uri = '{}/v4/layers/scoutingObservations/{}'.format(
        api_uri, scouting_observation_id)
    headers = {
        'authorization': bearer_token(token),
        'accept': json_content_type,
        'x-api-key': api_key
    }

    res = requests.get(uri, headers=headers)
    Logger().info(to_curl(res.request))

    if res.status_code == 200:
        return res.json()

    log_http_error(res)
    return None


def get_scouting_observation_attachments(token,
                                         api_key,
                                         scouting_observation_id):
    """
    Retrieve attachments associated with a given scouting observation. Photos
    added to scouting notes in the FieldView app are capped to 20MB, and we
    won’t store photos larger than that in a scouting note.
    https://dev.fieldview.com/technical-documentation/ for possible status
    values and their meaning.
    :param token: access_token
    :param api_key: Provided by Climate
    :param scouting_observation_id: Unique identifier of the
        Scouting Observation.

    """
    uri = '{}/v4/layers/scoutingObservations/{}/attachments'.format(
        api_uri, scouting_observation_id)
    headers = {
        'authorization': bearer_token(token),
        'accept': json_content_type,
        'x-api-key': api_key
    }

    res = requests.get(uri, headers=headers)
    Logger().info(to_curl(res.request))

    if res.status_code == 200:
        return res.json()['results']

    log_http_error(res)
    return []


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


def get_scouting_observation_attachments_contents(token,
                                                  api_key,
                                                  scouting_observation_id,
                                                  attachment_id,
                                                  content_type,
                                                  length):
    """
    Retrieve the binary contents of a scouting observation’s attachment.
    https://dev.fieldview.com/technical-documentation/ for possible status
    values and their meaning.
    :param token: access_token
    :param api_key: Provided by Climate
    :param scouting_observation_id: Unique identifier of the Scouting
        Observation.
    :param attachment_id : Unique identifiler of the attachment

    """

    uri = '{}/v4/layers/scoutingObservations/{}/attachments/{}/contents'.\
        format(api_uri,
               scouting_observation_id,
               attachment_id)

    headers = {
        'authorization': bearer_token(token),
        'accept': content_type,
        'x-api-key': api_key,
    }

    return fetch_contents(uri, headers, length)


def get_as_planted(token, api_key, next_token):
    """
    Retrieve as Planted activities
    :param token: access_token
    :param api_key: Provided by Climate
    :param next_token: Opaque string which allows for fetching the next batch
        of results.
    """
    return get_activities(token, api_key, next_token, "asPlanted")


def get_as_harvested(token, api_key, next_token):
    """
    Retrieve as Harvested activities
    :param token: access_token
    :param api_key: Provided by Climate
    :param next_token: Opaque string which allows for fetching the next batch
        of results.
    """

    return get_activities(token, api_key, next_token, "asHarvested")


def get_as_applied(token, api_key, next_token):
    """
    Retrieve as Applied activities
    :param token: access_token
    :param api_key: Provided by Climate
    :param next_token: Opaque string which allows for fetching the next batch
        of results.
    """

    return get_activities(token, api_key, next_token, "asApplied")


def get_activities(token, api_key, next_token, activity):
    """
    Retrieve a list of field activities.
    https://dev.fieldview.com/technical-documentation/ for possible status
    values and their meaning.
    :param token: access_token
    :param api_key: Provided by Climate
    :param next-token: Opaque string which allows for fetching the next batch
        of results.
    :param activity: name of activity

    """
    uri = '{}/v4/layers/{}'.format(api_uri, activity)

    headers = {
        'authorization': bearer_token(token),
        'x-api-key': api_key,
        'x-next-token': next_token,
        'x-limit': str(10)
    }

    res = requests.get(uri, headers=headers)

    if res.status_code == 200:
        return None, res.json()['results']
    if res.status_code == 206:
        return res.headers['x-next-token'], res.json()['results']
    if res.status_code == 304:
        return None, None

    log_http_error(res)

    return None, None


def get_activity_contents(token, api_key, layer_id, activity_id, length):
    """
    Retrieve a content of field activity.
    https://dev.fieldview.com/technical-documentation/ for possible status
    values and their meaning.
    :param token: access_token
    :param api_key: Provided by Climate
    :param layer_id: name of activity
    :param activity_id: id of activity
    :param length: content length

    """
    uri = '{}/v4/layers/{}/{}/contents'.format(api_uri, layer_id, activity_id)

    headers = {
        'authorization': bearer_token(token),
        'x-api-key': api_key,
    }

    return fetch_contents(uri, headers, length)


def fetch_contents(uri, headers, length):
    chunk_size = 1 * 1024 * 1024
    for start in range(0, length, chunk_size):
        end = min(length, start + chunk_size)
        headers['Range'] = 'bytes={}-{}'.format(start, end - 1)
        res = requests.get(uri, headers=headers)
        if res.status_code == 200 or res.status_code == 206:
            yield res.content
        else:
            log_http_error(res)
            break
