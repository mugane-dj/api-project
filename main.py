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
        self.song_info = {}
        self.youtube_playlist_id = youtube_playlist_id

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
        print("client fetching successful!")
        return youtube_client

    def get_playlist_items(self):
        youtube_client = self.get_youtube_client()
        request = youtube_client.playlistItems().list(
            part="snippet",
            playlistId=self.youtube_playlist_id,
            maxResults=30
        )
        response = request.execute()
        print(response)
        print("Looping through playlist...")
        for item in response["items"]:
            video_Id = item["snippet"]["resourceId"]["videoId"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(video_Id)
            video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False, force_generic_extractor=True, process=True)
            creator = video["title"]
            artist = creator.split("-")[0]   
            print(artist)
            track = video["title"]
            song_name = track.split("-")[1].split("| A COLORS SHOW")[0]
            print(song_name) 
        for item in response["items"]:
            video_title = item["snippet"]["title"]
        if song_name is not None and artist is not None:
            self.song_info[video_title] = {
                "youtube_url": youtube_url,
                "song_name": song_name,
                "artist": artist,
                "spotify_uri": self.get_spotify_uri(song_name, artist)
            }
        return song_name,artist,video_title

    def create_playlist(self):
        """Create A Playlist in Spotify"""
        self.refresh()
        request_body = json.dumps({
            "name": "Living Color",
            "description": "All songs in colors youtube playlist",
            "public": False
        })
        print("Creating spotify playlist")
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
        self.refresh()
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
        print(response_json["tracks"])
        songs = response_json["tracks"]["items"]
        uri = songs[0]["uri"]
        return uri 

    def add_songs_to_spotify_playlist(self):
        self.get_playlist_items()
        uris = [info["spotify_uri"]for song, info in self.song_info.items()]
        playlist_id = self.create_playlist()
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)
        print("Finalizing...")
        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        print(response)

    def refresh(self):
        refreshCaller = Refresh_token()
        self.spotify_token = refreshCaller.refresh()


if __name__ == '__main__':
    a = Playlist()
    a.add_songs_to_spotify_playlist()
