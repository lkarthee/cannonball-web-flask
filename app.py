from flask import Flask
from flask import request, render_template, jsonify

from urlparse import urlparse
import requests
import json

import config

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
            'index.html',
            DIGITS_CONSUMER_KEY=config.DIGITS_CONSUMER_KEY,
            GA_TRACKING_ID=config.GA_TRACKING_ID)


@app.route('/digits', methods=['POST',])
def digits():
    api_url = request.form['apiUrl']
    credentials = request.form['credentials']
    messages = []

    phone_number = ''
    user_id = ''
    error_message = ''

    verified = True
    # Verify the OAuth consumer key
    if 'oauth_consumer_key="'+config.DIGITS_CONSUMER_KEY+'"' not in credentials:
        verified = False
        messages.append('The Digits API key does not match.')

    hostname = urlparse(api_url).hostname
    if hostname != 'api.digits.com' and hostname != 'api.twitter.com':
        verified = False
        messages.append('Invalid API hostname.')

    if verified is False:
        return jsonify(phoneNumber=phone_number, userID=user_id, error=str(messages))

    headers = {
        'Authorization': credentials
    }
    response = requests.get(api_url, headers=headers)
    resp_json = response.json()
    
    return jsonify(phoneNumber=resp_json['phone_number'], userID=resp_json['id_str'], error='')

@app.route('/error')
def error():
    error_status = 'error_status'
    error_stack = 'error_stack'
    message = 'error_message'
    return render_template(
        'error.html',
        error_status=error_status,
        error_stack=error_stack,
        message=message)

if __name__ == '__main__':
    app.run(debug=True)
