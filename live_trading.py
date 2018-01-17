import requests
import base64
import hmac
import hashlib
import time
import json

""" api_keys is a python file consisting solely of variables where I store my api keys so I don't accidentally reveal
    them to everyone on github. Comment out or delete the following lines of code that contain those keys,
    then uncomment the two comments following that to include your own api keys. Be careful not to show anyone those
    keys! If you accidentally reveal them, you can delete your api keys from your Gemini account and get new ones."""
from api_keys import sandbox_api_secret  # delete this and uncomment the lines below
from api_keys import sandbox_api_key  # delete this and uncomment the lines below

# sandbox_api_key = 'insert your api public key here'
# sandbox_api_secret = b'insert your api secret key here'

sandbox_url = 'https://api.sandbox.gemini.com/v1/balances'



nonce = int(time.time() * 1000)

json_string = json.dumps({'request': '/v1/balances', 'nonce': nonce})

b64 = base64.b64encode(json_string.encode())

signature = hmac.new(sandbox_api_secret, b64, hashlib.sha384).hexdigest()

headers = {
    'Content-Type': "text/plain",
    'Content-Length': "0",
    'X-GEMINI-APIKEY': sandbox_api_key,
    'X-GEMINI-PAYLOAD': b64,
    'X-GEMINI-SIGNATURE': signature,
    'Cache-Control': "no-cache"
}

response = requests.request("POST", sandbox_url, headers=headers)

print(response.text)
