import os
import json
import requests

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

from secrets import spotify_user_id
from refreshtoken import Refresh_token
class Playlist:
    def __init__(self):
        self.spotify_token = ""
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    def get_youtube_client(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        client_secret = "client.json"
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secret, scopes)
        credentials = flow.run_local_server(port=8080, prompt="consent")
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        return youtube_client
        

    def get_playlist_items(self):
        request = self.youtube_client.playlistItems().list(
            part="snippet",
            playlistId="PLd2G12g_chuQ2T7Lzu9ZHoLLOA4T9hdGL"
        )
        reponse = request.execute()

        for items in reponse["items"]:
            video_title = item["snippets"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item["id"])
            video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False)
            song_name = video["track"]
            artist = video["artist"]
        if song_name is not None and artist is not None:
            self.all_song_info[video_title] = {
                "youtube_url": youtube_url,
                "song_name": song_name,
                "artist": artist,
                "spotify_uri": self.get_spotify_uri(song_name, artist)
            }
    def create_playlist(self):
        """Create A Playlist in Spotify"""
        request_body = json.dumps({
            "name": "GRM DAILY",
            "description": "All songs in GRM daily youtube playlist",
            "public": False
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        return response_json["id"]

    def get_spotify_uri(self, song_name, artist):
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        uri = songs[0]["uri"]
        return uri
    
    def add_songs_to_spotify_playlist(self):
        self.get_playlist_items()
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]
        playlist_id = self.create_playlist()
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
    def refresh(self):
        refreshCaller = refresh()
        self.spotify_token = refreshCaller.refresh()

if __name__ == '__main__':
    a = Playlist()
    a.add_songs_to_spotify_playlist()


