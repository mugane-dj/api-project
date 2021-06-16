#pylint: disable=E1101
import os
import json
import requests

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

from secrets import spotify_user_id, youtube_playlist_id
from refresh import Refresh_token
class Playlist:
    def __init__(self):
        self.spotify_token = ""
        self.song_info = ""
        self.youtube_playlist_id  = youtube_playlist_id 
    
    def get_youtube_client(self):
        print("Fetching client...")
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        client_secret = "youtube.json"
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secret, scopes)
        credentials = flow.run_local_server(port=8080, prompt="consent")
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        return youtube_client

    def get_playlist_items(self):
        youtube_client = self.get_youtube_client()
        request = youtube_client.playlistItems().list(
            part="snippet",
            playlistId=self.youtube_playlist_id 
        )
        reponse = request.execute()
        print("Looping through playlist...")
        for i in reponse["items"]:
            video_title = i["snippets"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                i['id'])
            video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False)
            song_name = video["track"]
            artist = video["artist"]
        if song_name is not None and artist is not None:
            self.song_info[video_title] = {
                "youtube_url": youtube_url,
                "song_name": song_name,
                "artist": artist,
                "spotify_uri": self.get_spotify_uri(song_name, artist)
            }

    def create_playlist(self):
        """Create A Playlist in Spotify"""
        self.refresh()
        print("Creating spotify playlist")
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
        return response_json['id']

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
        for i in response_json['items']:
            self.song_info += (i['track']['uri'], ',')
        self.song_info = self.song_info[:-1]
    
    def add_songs_to_spotify_playlist(self):
        print("Finalizing...")
        self.get_playlist_items()
        uris = self.song_info
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
        return response
    def refresh(self):
        refreshCaller = Refresh_token()
        self.spotify_token = refreshCaller.refresh()

if __name__ == '__main__':
    a = Playlist()
    a.add_songs_to_spotify_playlist()


