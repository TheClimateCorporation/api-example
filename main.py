"""
Partner example app

Start a simple app server:
 - allow user login via Climate
 - display user's Climate fields
 - retrieve field boundary info
 - basic file upload to Climate

Note: for this example, only one "user" can be logged into the example app
at a time.

License:
Copyright © 2017 The Climate Corporation
"""

import json

from flask import Flask, request, redirect, url_for
import climate

# config

client_id = ''     # OAuth2 client ID
client_secret = '' # OAuth2 client secret
api_key = ''       # X-Api-Key

def redirect_uri():
    return url_for('login_redirect', _external=True)

# partner app server

app = Flask(__name__)

# user state

_state = {}

def set_state(token=None, user=None, fields=[]):
    global _state
    _state = {
        'user': user,
        'token': token,
        'fields': fields
    }

set_state()

def state(key):
    global _state
    return _state.get(key)

# routes

@app.route('/login-redirect')
def login_redirect():
    code = request.args['code']
    if code:
        resp = climate.authenticate(code,
                                    client_id,
                                    client_secret,
                                    redirect_uri())
        if resp:
            # fetch index data
            token = resp['access_token']
            fields = climate.get_fields(token, api_key)

            # set app state
            set_state(user=resp['user'], token=token, fields=fields)

    return redirect(url_for('home'))

@app.route('/logout-redirect')
def logout_redirect():
    set_state()
    return redirect(url_for('home'))

def new_homepage():
    url = climate.login_uri(client_id, redirect_uri())
    return '<p><a href="{}">Login with Climate</a></p>'.format(url)

def render_ul(xs):
    return '<ul>{}</ul>'.format('\n'.join('<li>{}</li>'.format(x) for x in xs))

@app.route('/field/<field_id>')
def field(field_id):
    field = [f for f in state('fields') if f['id'] == field_id][0]

    boundary = climate.get_boundary(field['boundaryId'],
                                    state('token'),
                                    api_key)

    return """
           <p>{name}</p>
           <p>Boundary info:<pre>{boundary}</pre></p>
           <p><a href="{home}">Return home</a></p>
           """.format(name=field['name'],
                      boundary=json.dumps(boundary, indent=4, sort_keys=True),
                      home=url_for('home'))

def render_field_link(field):
    field_id = field['id']
    return '<a href="{link}">{name} ({id})</a>'.format(
        link=url_for('field', field_id=field_id),
        name=field['name'],
        id=field_id)

def user_homepage():
    field_list = render_ul(render_field_link(f) for f in state('fields'))
    return """
           <p>Hello, {first} {last}</p>
           <p><a href="{upload}">Upload data</a></p>
           <p>Your Climate fields:{fields}</p>
           <p><a href="{logout}">Log out</a></p>
           """.format(first=state('user')['firstname'],
                      last=state('user')['lastname'],
                      fields=field_list,
                      upload=url_for('upload_form'),
                      logout=url_for('logout_redirect'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_form():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('upload_form'))

        f = request.files['file']
        content_type = request.form['file_content_type']
        success = climate.upload(f, content_type, state('token'), api_key)

        return """
               <p>Upload data</p>
               <p>File uploaded: {success}</p>
               <p><a href="{home}">Return home</a></p>
               """.format(success=success, home=url_for('home'))

    return """
           <p>Upload data</p>
           <form method=post enctype=multipart/form-data>
           <p>Content type:<input type=text name=file_content_type /></p>
           <p><input type=file name=file /></p>
           <p><input type=submit value=Upload /></p>
           </form>
           <p><a href="{home}">Return home</a></p>
           """.format(home=url_for('home'))

@app.route('/home')
def home():
    if state('user'):
        return user_homepage()
    else:
        return new_homepage()

# start app

if __name__ == '__main__':
    app.run(
        host="localhost",
        port=8080
    )
