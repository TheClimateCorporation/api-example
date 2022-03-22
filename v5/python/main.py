"""
Partner example app

Start a simple app server:
 - allow user login via Climate
 - retrieve harvest activity
 - retrieve growing seasons

We use Flask in this example to provide a simple HTTP server. You will notice
that some of the functions in this file are decorated with @app.route() which
registers them with Flask as functions to service requests to the specified
URIs.

This file (main.py) provides the web UI and framework for the demo app. All
the work with the Climate API happens in climate.py.

Note: For this example, only one "user" can be logged into the example app at
a time.

License:
Copyright © 2018 The Climate Corporation
"""

import json
import os
from logger import Logger

from flask import Flask, request, redirect, url_for
import climate

# Configuration of your Climate partner credentials. This assumes you have
# placed them in your environment. You may
# also choose to just hard code them here if you prefer.

CLIMATE_API_ID = os.environ['CLIMATE_API_ID']         # OAuth2 client ID
CLIMATE_API_SECRET = os.environ['CLIMATE_API_SECRET']   # OAuth2 client secret
CLIMATE_API_SCOPES = os.environ['CLIMATE_API_SCOPES']  # Oauth2 scope list
CLIMATE_API_KEY = os.environ['CLIMATE_API_KEY']       # X-Api-Key header
# Partner app server

app = Flask(__name__)
logger = Logger(app.logger)

# User state - only one user at a time. In your application this would be
# handled by your session management and backing
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


def clear_state():
    set_state(access_token=None, refresh_token=None, user=None, fields=None)


def state(key):
    global _state
    return _state.get(key)

# Routes


@app.route('/')
def home():
    if state('user'):
        return user_homepage()
    return no_user_homepage()


def no_user_homepage():
    """
    This is logically the first place a user will come. On your site it will
    be some page where you present them with a link to Log In with FieldView.
    The main thing here is that you provide a correctly formulated link with
    the required parameters and correct button image.
    :return: None
    """
    url = climate.login_uri(CLIMATE_API_ID, CLIMATE_API_SCOPES, redirect_uri())
    return """
            <h1>Partner API Demo Site</h1>
            <h2>Welcome to the Climate Partner Demo App.</h2>
            <p>Imagine that this page is your great web application and you
            want to connect it with Climate FieldView. To do this, you need
            to let your users establish a secure connection between your app
            and FieldView. You do this using Log In with FieldView.</p>
            <p style="text-align:center"><a href="{}">
            <img src="./static/fv-login-button.png"
            alt="FieldView Login"></a></p>""".format(url)


def user_homepage():
    """
    This page just demonstrates some basic Climate FieldView API operations
    such as getting field details, accessing user information and and
    refreshing the authorization token.
    :return: None
    """
    return """
           <h1>Partner API Demo Site</h1>
           <p>User name retrieved from FieldView: {first} {last}</p>
           <p>Access Token: {access_token}</p>
           <p>Refresh Token: {refresh_token}
           (<a href="{refresh}">Refresh</a>)</p>
           <table style="border-spacing: 50px 0;"><tr><td>
           <p><a href="{growing_seasons}">Growing Seasons</a></p>
           <p><a href="{harvest_reports}">Harvest Reports</a></p>
           </td></tr></table>
           <p><a href="{logout}">Log out</a></p>
           """.format(first=state('user')['firstname'],
                      last=state('user')['lastname'],
                      access_token=state('access_token'),
                      refresh_token=state('refresh_token'),
                      refresh=url_for('refresh_token'),
                      logout=url_for('logout_redirect'),
                      growing_seasons=url_for('growing_seasons'),
                      harvest_reports=url_for('harvest_reports'))


@app.route('/login-redirect')
def login_redirect():
    """
    This is the page a user will come back to after having successfully logged
    in with FieldView. The URI was provided as one of the parameters to the
    login URI above. The "code" parameter in the URI's query string contains
    the access_token and refresh_token.
    :return:
    """
    code = request.args['code']
    if code:
        resp = climate.authorize(code,
                                 CLIMATE_API_ID,
                                 CLIMATE_API_SECRET,
                                 redirect_uri())
        if resp:
            # Store tokens and user in state for subsequent requests.
            access_token = resp['access_token']
            refresh_token = resp['refresh_token']
            set_state(user=resp['user'],
                      access_token=access_token,
                      refresh_token=refresh_token)

    return redirect(url_for('home'))


def redirect_uri():
    """
    :return: Returns uri for redirection after Log In with FieldView.
    """
    return url_for('login_redirect', _external=True)


@app.route('/refresh-token')
def refresh_token():
    """
    This route doesn't have any page associated with it; it just refreshes the
    authorization token and redirects back to the home page. As a by-product,
    this also refreshes the user data.
    :return:
    """
    resp = climate.reauthorize(state('refresh_token'),
                               CLIMATE_API_ID,
                               CLIMATE_API_SECRET)
    if resp:
        # Store tokens and user in state for subsequent requests.
        access_token = resp['access_token']
        refresh_token = resp['refresh_token']
        set_state(user=resp['user'], access_token=access_token,
                  refresh_token=refresh_token)

    return redirect(url_for('home'))


@app.route('/logout-redirect')
def logout_redirect():
    """
    Clears all current user data. Does not make any Climate API calls.
    :return:
    """
    clear_state()
    return redirect(url_for('home'))


@app.route('/growingSeasons', methods=['GET', 'POST'])
def growing_seasons():
    """
    Initially (when method=GET) render the growing seasons form to collect
    information necessary for the growingSeasons request. When the form is
    POSTed, invoke the actual Climate API.
    :return: HTML form or the Growing Seasons Id
    """
    if request.method == 'POST':
        field_id = request.form['field_id']
        growing_seasons_id = climate.growingSeasons(
            field_id, state('access_token'), CLIMATE_API_KEY)
        growing_seasons_contents_url = url_for(
            'growing_seasons_contents', growing_seasons_id=growing_seasons_id)

        return """
            <h1>Partner API Demo Site</h1>
            <h2>Growing Seasons</h2>
            <p>Growing Seasons Ids: <a href="{growing_seasons_contents_url}">
            {growing_seasons_id}</a></a>
            <p><a href="{home}">Return home</a></p>
            """.format(
            growing_seasons_contents_url=growing_seasons_contents_url,
            growing_seasons_id=growing_seasons_id,
            home=url_for('home'))

    return """
           <h1>Partner API Demo Site</h1>
           <h2>Growing Seasons</h2>
           <form method=post>
           <p>Field ID: <input type=text name=field_id /></p>
           <p><input type=submit value=Submit /></p>
           </form>
           <p><a href="{home}">Return home</a></p>
           """.format(home=url_for('home'))


@app.route('/growingSeasonsContents/<growing_seasons_id>', methods=['GET'])
def growing_seasons_contents(growing_seasons_id):
    """
    This page shows the growing seasons content id and year of the growing
    season
    :return: response from Climate's GrowingSeasonsConents API
    """
    response = climate.growingSeasonsContents(
        growing_seasons_id, state('access_token'), CLIMATE_API_KEY)
    return """<h1>Partner API Demo Site</h1>
            <h2>Growing Seasons Contents</h2>
            <pre>{response}</pre>
            <p><a href="{home}">Return home</a></p>""".format(
        response=response, home=url_for('home'))


@app.route('/harvestReports', methods=['GET', 'POST'])
def harvest_reports():
    """
    Initially (when method=GET) render the harvest reports form to collect
    information necessary for the harvestReports request. When the form is
    POSTed, invoke the actual Climate API.
    :return: HTML form or the Harvest Reports Id
    """
    if request.method == 'POST':
        field_id = request.form['field_id']
        seasons = request.form['seasons'].replace(' ', '').split(',')
        harvest_report_id = climate.harvestReports(
            field_id, seasons, state('access_token'), CLIMATE_API_KEY)
        harvest_report_contents_url = url_for(
            'harvest_report_contents', harvest_report_id=harvest_report_id)

        return """
            <h1>Partner API Demo Site</h1>
            <h2>Harvest Report</h2>
            <p>Harvest Report Id: <a href="{harvest_report_contents_url}">
            {harvest_report_id}</a></p>
            <p><a href="{home}">Return home</a></p>
            """.format(harvest_report_contents_url=harvest_report_contents_url,
                       harvest_report_id=harvest_report_id,
                       home=url_for('home'))
    return """
           <h1>Partner API Demo Site</h1>
           <h2>Harvest Report</h2>
           <form method=post>
           <p>Field ID: <input type=text name=field_id /></p>
           <label for="seasons">Growing Seasons (comma delimited):</label>
           <textarea name=seasons rows="4" cols="50"/></textarea>
           <p><input type=submit value=Submit /></p>
           </form>
           <p><a href="{home}">Return home</a></p>
           """.format(home=url_for('home'))


@app.route('/harvestReportsContents/<harvest_report_id>', methods=['GET'])
def harvest_report_contents(harvest_report_id):
    """
    This page shows the harvest reports of the inputted growing seasons
    :return: response from Climate's harvestReportsContents API
    """
    response = climate.harvestReportsContents(
        harvest_report_id, state('access_token'), CLIMATE_API_KEY)
    return """<h1>Partner API Demo Site</h1>
            <h2>Harvest Reports Contents</h2>
            <pre>{response}</pre>
            <p><a href="{home}">Return home</a></p>""".format(
        response=response, home=url_for('home'))


# start app


if __name__ == '__main__':
    clear_state()
    app.run(
        host="localhost",
        port=8080
    )
