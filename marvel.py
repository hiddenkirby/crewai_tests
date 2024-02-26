# TODO: Move this into tools

import hashlib
import requests
import datetime
import ssl
import os
from langchain.tools import tool

@tool
def fetch_marvel_characters(clue):
    """Fetch Marvel characters with specified limit and series, returning their names"""
    pub_key = os.getenv('MARVEL_PUBLIC_KEY', 'default_public_key')
    priv_key = os.getenv('MARVEL_PRIVATE_KEY', 'default_private_key')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')

    def hash_params():
        """Generate md5 hash of timestamp, public key, and private key."""
        hash_md5 = hashlib.md5()
        hash_md5.update(f'{timestamp}{priv_key}{pub_key}'.encode('utf-8'))
        return hash_md5.hexdigest()

    class TLSAdapter(requests.adapters.HTTPAdapter):
        """TLS Adapter for specifying cipher suites."""
        def init_poolmanager(self, *args, **kwargs):
            ctx = ssl.create_default_context()
            ctx.set_ciphers("AES128-SHA256")
            kwargs["ssl_context"] = ctx
            return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)

    url = "https://gateway.marvel.com:443/v1/public/characters"
    params = {
        'ts': timestamp,
        'limit': 100,
        'series': '1987',
        'apikey': pub_key,
        'hash': hash_params()
    }

    with requests.session() as s:
        s.mount("https://", TLSAdapter())
        response_json = s.get(url, params=params).json()

    
    characters = response_json['data']['results']
    filtered_characters = [{"name": character["name"], "description": character["description"]} for character in characters]
    print(filtered_characters)
    return filtered_characters

fetch_marvel_characters('A Spider web')