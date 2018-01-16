import requests
import base64
import hmac
import hashlib
import time
import json

sandbox_url = 'https://api.sandbox.gemini.com/v1/balances'

sandbox_api_key = '5iRHvlg0VdOXs0osOVer'
sandbox_api_secret = b'S6rBJsdDvG2mPZtxSbqksMT5bZu'


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
