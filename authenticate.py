from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

"""
Authentication Class
1. list scopes, put all into a list
2. load environment variables from dotenv
3. Call OAuth function (figure out way to get url redirect)
"""

scope_list = ["user-library-read", "user-read-recently-played", "playlist-modify-private"]

class Authenticate:
    def __init__(self, scope):
        load_dotenv()
        self.scope = scope
        #spotipy client
        self.spotipy = Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def get_spotipy_client(self):
        return self.spotipy

def list_scopes():
    for i, scope in enumerate(scope_list):
        print(i, scope)
    answer = [int(n) for n in input("gib ").split()]
    result = [scope_list[i] for i in answer]
    return result