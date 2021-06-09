import os
import json
import requests

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl


class Playlist:
    def __init__(self):
        self.youtube_client = self.get_youtube_client


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

if __name__ == '__main__':
    a = Playlist()
    a.get_youtube_client()






#["https://www.googleapis.com/youtube/v3/playlistItems"]

