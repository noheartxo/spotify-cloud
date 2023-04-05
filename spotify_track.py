from datetime import datetime, date

class Spotify:
    def __init__(self, spotipy):
        # client
        self.spotipy = spotipy
        self.user_id = spotipy.me()['id']

    def get_user_id(self):
        return self.user_id

    def get_uri(self, items):
        return [uri.get_uri() for uri in items]

    """
    Gets the total number of liked songs for the current user
    """
    def get_number_of_tracks(self) -> int:
        return int(self.spotipy.current_user_saved_tracks(limit=1)['total'])

    """
    Extracts the uri for a track

    parameters:
        - results (list): Collected information about tracks

    returns:
        - list: Track URIs
    """
    def get_track_info(self, results: list) -> list:
        track_list = []
        for item in results['items']:
            uri = item['track']['uri']
            track_list.append(uri)
        return track_list

    """
    Gets all liked songs in "Your Music"
    """
    def get_liked_songs(self):
        offset = 0
        track_list = []
        while True:
            results = self.spotipy.current_user_saved_tracks(limit=50, offset=offset)
            if results['items'] == []:
                break
            else: 
                track_list.extend(self.get_track_info(results))
                offset += 50
        return track_list
    
    """
    Gets 50 most recently played songs
    """
    def get_recently_played(self):
        results = self.spotipy.current_user_recently_played()
        track_list = self.get_track_info(results)
        return track_list
    
    """
    Gets all the tracks within a playlist given the id; will verify if the tracks are old 
    """
    def get_playlist_tracks(self, playlist_id: str, fields="items(added_at, track(uri))", verify_dates=False) -> list:
        offset = 0
        playlist_tracks = []
        while True:
            results = self.spotipy.playlist_items(playlist_id, fields, offset=offset)
            if results['items'] == []:
                break
            else:
                if verify_dates:
                    playlist_tracks.extend(self.verify_dates(results))
                else:
                    playlist_tracks.extend(self.get_track_info(results))
                offset += 50
        return playlist_tracks

    """
    Creates a playlist given a playlist name
        - unsure if this is a bug with spotipy, but the playlists are obly created publicly even 
        if you specify otherwise
    """
    def create_playlist(self, playlist_name: str, public=False) -> str:
        result = self.spotipy.user_playlist_create(self.user_id, playlist_name, public=public)
        return result['uri']

    """
    Adds tracks to a playlist given a playlist_id and list of track uris
    """
    def add_items_to_playlist(self, playlist_id: str, items: list):
        to_be_added = self.get_uri(items)
        self.spotipy.playlist_add_items(playlist_id, to_be_added)

    """
    Deletes tracks from a playlist given a playlist_id and list of track uris
    """
    def remove_playlist_tracks(self, playlist_id: str, items: list):
        to_be_removed = self.get_uri(items)
        self.spotipy.playlist_remove_all_occurrences_of_items(playlist_id, to_be_removed)
    
    """
    Utilized to see if dates are older than today's date as it will be run once a week
    """
    def verify_dates(self, results: list) -> list:
        verified = []
        date_today = date.today()
        for item in results['items']:
            added_at = datetime.strptime(item['added_at'][0:10], "%Y-%m-%d").date()
            if date_today >= added_at:
                track = item['track']['uri']
                verified.append(track)
        return verified