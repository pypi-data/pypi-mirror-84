import json
import logging

from flask import Flask, request

from arivo import webhook

app = Flask(__name__)

webhook_secret = ""


@app.route('/webhook', methods=["POST"])
def receive_webhook():
    payload = request.get_data()
    signature = request.headers.get('X-Signature')
    try:
        event = webhook.construct_event(payload, signature, webhook_secret)
    except webhook.InvalidPayload as e:
        logging.error("Invalid webhook payload: %s", payload)
    except webhook.InvalidSignature as e:
        logging.error("Invalid webhook signature")
    else:
        print(json.dumps(event, indent=4))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
