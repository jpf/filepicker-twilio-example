import os
from twilio.rest import TwilioRestClient
from flask import Flask, request, render_template

twilio_account_sid = ''
twilio_auth_token = ''
twilio_from_number = ''
filepicker_api_key = ''

app = Flask(__name__)
client = TwilioRestClient(twilio_account_sid, twilio_auth_token)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        client.sms.messages.create(
            to=request.form['phone_number'],
            from_=twilio_from_number,
            body="Check this out: %s?dl=false" % request.form['file'])
    fp_key = filepicker_api_key
    return render_template('simple.html', filepicker_api_key=fp_key)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
