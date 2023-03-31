from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

scope_list = ["ugc-image-upload", "user-read-playback-state", "user-modify-playback-state", 
              "user-read-currently-playing", "app-remote-control", "streaming", "playlist-read-private", 
              "playlist-read-collaborative", "playlist-modify-private", "playlist-modify-public", "user-follow-modify", 
              "user-follow-read", "user-read-playback-position", "user-top-read", "user-read-recently-played", 
              "user-library-modify", "user-library-read", "user-read-email", "user-read-private"]

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