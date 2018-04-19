import flask
from flask import request, redirect
from urllib.parse import quote_plus
import requests


APP_ID = 'b4a9de93-08df-4237-9b01-4ea1a5730c22'
APP_PASS = 'jfgrYBRKQ4^]zqtJJ5917}$'

# Id: 546640d4-92d3-49b4-bf4d-991edc072f6f
# Password: jvvTP5281}+nwaxMORJI1_|

AUTH_CODE_REQ = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={app_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=openid%20offline_access%20https%3A%2F%2Fgraph.microsoft.com%2Fmail.read&state=12345&sso_reload=true'

app = flask.Flask(__name__, template_folder='static/templates')
# APP.debug = True
# APP.secret_key = 'development'

@app.route('/')
def main():
    auth_code_req_redirect_url = quote_plus(request.url_root + 'login/authorized')
    redirect_url = AUTH_CODE_REQ.format(app_id=APP_ID, redirect_uri=auth_code_req_redirect_url)
    return redirect(redirect_url)

@app.route('/login/authorized')
def xxx():
    if 'code' not in request.args: #error
        return request.query_string
    
    #get access token
    auth_code = request.args.get("code")
    auth_code_req_redirect_url = request.url_root + 'login/authorized'
    data = dict(
            client_id=APP_ID,
            scope='https://graph.microsoft.com/mail.read',
            redirect_uri=auth_code_req_redirect_url,
            grant_type='authorization_code',
            client_secret=APP_PASS,
            code=auth_code
        )
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    response = response.json()

    if 'access_token' not in response: #error
        return flask.jsonify(response)

    #get data from api
    access_token = response.get('access_token')
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get('https://graph.microsoft.com/v1.0/me/messages?$select=subject,bodyPreview,from,sender,receivedDateTime&$top=10&$orderby=receivedDateTime%20DESC', headers=headers)
    response = response.json()

    return flask.jsonify(response)

if __name__ == '__main__':
    app.run()