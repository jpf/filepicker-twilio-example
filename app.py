import os, re
from twilio.rest import TwilioRestClient
import sendgrid
from flask import Flask, request, render_template
app = Flask(__name__)

# TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables must be set
client = TwilioRestClient()

# SENDGRID_USER and SENDGRID_PASS enviornment variables must be set
sg = sendgrid.Sendgrid(os.environ.get('SENDGRID_USER'), os.environ.get('SENDGRID_PASS'), secure=True)

@app.route("/", methods=['POST', 'GET'])
def index():
    option = {}
    option['filepicker_api_key'] = os.environ.get('FILEPICKER_API_KEY')
    if request.method == 'POST':
        option['file'] = request.form['file']
        option['phone_number'] = request.form['phone_number']
        try:
          body = "Check out this picture: %s?dl=false" % option['file']

          if not re.match(r"[^@]+@[^@]+\.[^@]+", option['phone_number']):
            # Phone
            from_ = os.environ.get('TWILIO_FROM_NUMBER')
            client.sms.messages.create(to=option['phone_number'],
                                       from_=from_,
                                       body=body)
          else:
            # Email
            from_ = os.environ.get('SENDGRID_FROM_EMAIL')
            message = sendgrid.Message(from_, "Check out this picture", body, body)
            message.add_to(option['phone_number'])

            sg.web.send(message)

          option['message_sent'] = True
        except:
            option['message_sent'] = False
    return render_template('index.html', **option)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
