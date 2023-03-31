from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import requests
import base64
import json
import os

"""
Authentication Class
1. list scopes, put all into a list
2. load environment variables from dotenv
3. Call OAuth function (figure out way to get url redirect)
"""

scope_list = ["ugc-image-upload", "user-read-playback-state", "user-modify-playback-state", 
              "user-read-currently-playing", "app-remote-control", "streaming", "playlist-read-private", 
              "playlist-read-collaborative", "playlist-modify-private", "playlist-modify-public", "user-follow-modify", 
              "user-follow-read", "user-read-playback-position", "user-top-read", "user-read-recently-played", 
              "user-library-modify", "user-library-read", "user-read-email", "user-read-private"]

class Authenticate:
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"

    def __init__(self, scope):
        load_dotenv()
        self.scope = scope

        #spotipy client
        self.spotipy = Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def get_spotipy_client(self):
        return self.spotipy
    
    def request_new_token(self, cache_file):
        SPOTIPY_CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
        SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']

        with open(cache_file) as access_token:
            refresh_token = json.loads(access_token.read())['refresh_token']

        body = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        header_text = (SPOTIPY_CLIENT_ID + ":" + SPOTIPY_CLIENT_SECRET).encode('ascii')
        headers = {
            'Authorization': 'Basic %s' % ((base64.b64encode(header_text).decode('ascii')))
        }
        
        response = requests.post(self.OAUTH_TOKEN_URL, data=body, headers=headers)
        response = json.loads(response.text)

        # adds refresh_token to still be used
        response['refresh_token'] = refresh_token
        return response

def list_scopes():
    for i, scope in enumerate(scope_list):
        print(i, scope)
    answer = [int(n) for n in input("gib ").split()]
    result = [scope_list[i] for i in answer]
    return result