import requests
import base64

CONSUMER_KEY = "y8zzpd0fqzt8AvtCDTk9PwlXa3JJRfDd3A3o0OkXRaPmi1M8"
CONSUMER_SECRET = "Wb3xAH6LorAnyLhzDgl6ep9AW41WuvWtF89yoKdOkYhSoywPfGZCXPljUWRX5HJc"

SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97dd8b85e1e0b5e4b5b6d..."
CALLBACK_URL = "https://example.com/callback"

import requests
import base64


def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    auth = base64.b64encode(
        f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {auth}"
    }

    response = requests.get(url, headers=headers)

    print(response.status_code)
    print(response.text)

    return response.json()