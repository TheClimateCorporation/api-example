"""
Partner example app

Start a simple app server:
 - allow user login via Climate
 - display user's Climate fields
 - retrieve field boundary info
 - basic file upload to Climate

We use Flask in this example to provide a simple HTTP server. You will notice that some of the functions in this
file are decorated with @app.route() which registers them with Flask as functions to service requests to the
specified URIs.

This file (main.py) provides the web UI and framework for the demo app. All the work with the Climate API
happens in climate.py.

Note: For this example, only one "user" can be logged into the example app at a time.

License:
Copyright © 2017 The Climate Corporation
"""

import json
import os
from logger import Logger

from flask import Flask, request, redirect, url_for, send_from_directory
import climate

# Configuration of your Climate partner credentials. This assumes you have placed them in your environment. You may
# also choose to just hard code them here if you prefer.

client_id = os.environ['CLIMATE_API_ID']  # OAuth2 client ID
client_secret = os.environ['CLIMATE_API_SECRET']  # OAuth2 client secret
api_key = os.environ['CLIMATE_API_KEY']  # X-Api-Key


# Partner app server

app = Flask(__name__)
logger = Logger(app.logger)

# User state - only one user at a time. In your application this would be handled by your session management and backing
# storage.

_state = {}


def set_state(**kwargs):
    global _state
    if 'access_token' in kwargs:
        _state['access_token'] = kwargs['access_token']
    if 'refresh_token' in kwargs:
        _state['refresh_token'] = kwargs['refresh_token']
    if 'user' in kwargs:
        _state['user'] = kwargs['user']
    if 'fields' in kwargs:
        _state['fields'] = kwargs['fields']


def clear_state():
    set_state(access_token=None, refresh_token=None, user=None, fields=None)


def state(key):
    global _state
    return _state.get(key)


# Routes


@app.route('/home')
def home():
    if state('user'):
        return user_homepage()
    else:
        return no_user_homepage()


def no_user_homepage():
    """
    This is logically the first place a user will come. On your site it will be some page where you present them with
    a link to Log In with FieldView. The main thing here is that you provide a correctly formulated link with the
    required parameters and correct button image.
    :return: None
    """
    url = climate.login_uri(client_id, redirect_uri())
    return """
            <h1>Partner API Demo Site</h1>
            <h2>Welcome to the Climate Partner Demo App.</h2>
            <p>Imagine that this page is your great web application and you want to connect it with Climate FieldView.
            To do this, you need to let your users establish a secure connection between your app and FieldView. You
            do this using Log In with FieldView.</p>
            <p style="text-align:center"><a href="{}"><img src="./res/fv-login-button.png"></a></p>""".format(url)


def user_homepage():
    """
    This page just demonstrates some basic Climate FieldView API operations such as getting field details, accessing
    user information and and refreshing the authorization token.
    :return: None
    """
    field_list = render_ul(render_field_link(f) for f in state('fields'))
    return """
           <h1>Partner API Demo Site</h1>
           <p>User name retrieved from FieldView: {first} {last}</p>
           <p>Access Token: {access_token}</p>
           <p>Refresh Token: {refresh_token} (<a href="{refresh}">Refresh</a>)</p>
           <p>Your Climate fields:{fields}</p>
           <p><a href="{upload}">Upload data</a></p>
           <p><a href="{logout}">Log out</a></p>
           """.format(first=state('user')['firstname'],
                      last=state('user')['lastname'],
                      access_token=state('access_token'),
                      refresh_token=state('refresh_token'),
                      fields=field_list,
                      upload=url_for('upload_form'),
                      logout=url_for('logout_redirect'),
                      refresh=url_for('refresh_token'))


@app.route('/login-redirect')
def login_redirect():
    """
    This is the page a user will come back to after having successfully logged in with FieldView. The URI was provided
    as one of the parameters to the login URI above. The "code" parameter in the URI's query string contains the
    access_token and refresh_token.
    :return:
    """
    code = request.args['code']
    if code:
        resp = climate.authorize(code,
                                 client_id,
                                 client_secret,
                                 redirect_uri())
        if resp:
            # Store tokens and user in state for subsequent requests.
            access_token = resp['access_token']
            refresh_token = resp['refresh_token']
            set_state(user=resp['user'], access_token=access_token, refresh_token=refresh_token)

            # Fetch fields and store in state just for example purposes. You might well do this at the time of need,
            # or not at all depending on your app.
            fields = climate.get_fields(access_token, api_key)
            set_state(fields=fields)

    return redirect(url_for('home'))


@app.route('/refresh-token')
def refresh_token():
    """
    This route doesn't have any page associated with it; it just refreshes the authorization token and redirects back
    to the home page. As a by-product, this also refreshes the user data.
    :return:
    """
    resp = climate.reauthorize(state('refresh_token'),
                               client_id,
                               client_secret)
    if resp:
        # Store tokens and user in state for subsequent requests.
        access_token = resp['access_token']
        refresh_token = resp['refresh_token']
        set_state(user=resp['user'], access_token=access_token, refresh_token=refresh_token)

    return redirect(url_for('home'))


@app.route('/logout-redirect')
def logout_redirect():
    """
    Clears all current user data. Does not make any Climate API calls.
    :return:
    """
    clear_state()
    return redirect(url_for('home'))


@app.route('/field/<field_id>')
def field(field_id):
    """
    Shows how to fetch field boundary information and displays it as raw geojson data.
    :param field_id:
    :return:
    """
    field = [f for f in state('fields') if f['id'] == field_id][0]

    boundary = climate.get_boundary(field['boundaryId'],
                                    state('access_token'),
                                    api_key)

    return """
           <h1>Partner API Demo Site</h1>
           <h2>Field Name: {name}</h2>
           <p>Boundary info:<pre>{boundary}</pre></p>
           <p><a href="{home}">Return home</a></p>
           """.format(name=field['name'],
                      boundary=json.dumps(boundary, indent=4, sort_keys=True),
                      home=url_for('home'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_form():
    """
    Initially (when method=GET) render the upload form to collect information about the file to upload.
    When the form is POSTed, invoke the actual Climate API code to do the chunked upload.
    :return:
    """
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].stream is None:
            return redirect(url_for('upload_form'))

        f = request.files['file']
        content_type = request.form['file_content_type']
        upload_id = climate.upload(f, content_type, state('access_token'), api_key)

        return """
               <h1>Partner API Demo Site</h1>
               <h2>Upload data</h2>
               <p>File uploaded: {upload_id} <a href='{status_url}'>Get Status</a></p>
               <p><a href="{home}">Return home</a></p>
               """.format(upload_id=upload_id, status_url=url_for('update_status', upload_id=upload_id), home=url_for('home'))

    return """
           <h1>Partner API Demo Site</h1>
           <h2>Upload data</h2>
           <form method=post enctype=multipart/form-data>
           <p>Content type:<input type=text name=file_content_type /></p>
           <p><input type=file name=file /></p>
           <p><input type=submit value=Upload /></p>
           </form>
           <p><a href="{home}">Return home</a></p>
           """.format(home=url_for('home'))

@app.route('/upload/<upload_id>', methods=['GET'])
def update_status(upload_id):
    """
    Shows the status of an upload.
    :param upload_id:
    :return:
    """
    status = climate.get_upload_status(upload_id,
                                       state('access_token'),
                                       api_key)

    return """
           <h1>Partner API Demo Site</h1>
           <h2>Upload ID: {upload_id}</h2>
           <p>Status: {status} <a href="#" onclick="location.reload();">Refresh</a></p>
           <p><a href="{home}">Return home</a></p>
           """.format(upload_id=upload_id,
                      status=status.get('status'),
                      home=url_for('home'))


# Various utilities just to make the demo app work. No Climate API stuff here.


@app.route('/res/<path:path>')
def send_res(path):
    """
    Sends a static resource.
    """
    return send_from_directory('res', path)


def render_ul(xs):
    return '<ul>{}</ul>'.format('\n'.join('<li>{}</li>'.format(x) for x in xs))


def render_field_link(field):
    field_id = field['id']
    return '<a href="{link}">{name} ({id})</a>'.format(
        link=url_for('field', field_id=field_id),
        name=field['name'],
        id=field_id)


def redirect_uri():
    """
    :return: Returns uri for redirection after Log In with FieldView.
    """
    return url_for('login_redirect', _external=True)



# start app

if __name__ == '__main__':
    clear_state()
    app.run(
        host="localhost",
        port=8080
    )
