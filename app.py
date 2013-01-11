import os
from twilio.rest import TwilioRestClient
from flask import Flask, request, render_template
app = Flask(__name__)
# TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables must be set
client = TwilioRestClient()


@app.route("/", methods=['POST', 'GET'])
def index():
    option = {}
    option['filepicker_api_key'] = os.environ.get('FILEPICKER_API_KEY')
    if request.method == 'POST':
        option['file'] = request.form['file']
        option['phone_number'] = request.form['phone_number']
        try:
            from_ = os.environ.get('TWILIO_FROM_NUMBER')
            body = "Check out this picture: %s?dl=false" % option['file']
            client.sms.messages.create(to=option['phone_number'],
                                       from_=from_,
                                       body=body)
            option['sms_sent'] = True
        except:
            option['sms_sent'] = False
    return render_template('index.html', **option)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
