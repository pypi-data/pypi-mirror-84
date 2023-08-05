from urllib.parse import urlencode
import json

def call(client, path, params):
    url = path + '?' + urlencode(params)
    response = client.get(url)
    return json.loads(response.data.decode('utf-8'))

def test_login():
    pass