#imports
import os, json, requests
import google_auth_oauthlib.flow
import googleapiclient.discovery

import googleapiclient.errors
import youtube_dl
from pydash import py_

from core.refresh import refresh
from dotenv import load_dotenv
load_dotenv()

#global variables
spotify_user_id = os.getenv("spotify_user_id")
youtube_playlist_id = os.getenv("youtube_playlist_id")

spotify_token = ""
song_info = {}

def get_youtube_client() -> None:
    """
    We're using the google_auth_oauthlib library to authenticate our app with the Google API
    :return: The youtube client object
    """
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

    print(f"client fetching successful{youtube_client}!")

    return youtube_client

def get_spotify_token() -> None:
    """
    It gets a Spotify token
    """
    global spotify_token
    if spotify_token == "":
        spotify_token = refresh()
    

def get_spotify_uri(song_name: str, artist: str) -> str:
    """
    It takes in a song name and artist name, and returns the Spotify URI for the song
    
    :param song_name: The name of the song you want to add to the playlist
    :type song_name: str
    :param artist: The artist's name
    :type artist: str
    :return: The URI of the song
    """
    get_spotify_token()

    query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
        song_name,
        artist
    )

    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        })
    response_json = response.json()
    songs = response_json["tracks"]["items"]
    uri = songs[0]["uri"]
    return uri 

def get_playlist_items() -> None:
    """
    We're looping through the playlist items, extracting the video title, video ID, and YouTube URL.
    Then, we're using the YouTube URL to extract the video title, artist, and song name. Finally, we're
    using the song name and artist to get the Spotify URI
    """
    youtube_client = get_youtube_client()
    request = youtube_client.playlistItems().list(
        part="snippet",
        playlistId=youtube_playlist_id,
        maxResults=15
    )

    response = request.execute()

    print("Looping through playlist...")

    for item in response["items"]:
        video_title = item["snippet"]["title"]
        video_Id = py_.get(item, "snippet.resourceId.videoId")
        youtube_url = "https://www.youtube.com/watch?v={}".format(video_Id)
        video = youtube_dl.YoutubeDL({}).extract_info(
            youtube_url, download=False, force_generic_extractor=True)
        creator = video["title"]
        artist = creator.split("-")[0]   
        track = video["title"]
        song_name = track.split("-")[1].split("| A COLORS SHOW")[0]

        song_info[video_title] = {
            "youtube_url": youtube_url,
            "song_name": song_name,
            "artist": artist,
            "spotify_uri": get_spotify_uri(song_name, artist)
        }

def create_playlist() -> str:
    """
    It creates a playlist in Spotify with the name "Living Color" and the description "Songs in colors
    youtube playlist" and returns the id of the playlist
    :return: The id of the playlist created
    """
    """Create A Playlist in Spotify"""
    get_spotify_token()

    request_body = json.dumps({
        "name": "Living Color",
        "description": "Songs in colors youtube playlist",
        "public": False
    })

    print("Creating spotify playlist...")

    query = "https://api.spotify.com/v1/users/{}/playlists".format(
        spotify_user_id)

    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    response_json = response.json()
    return response_json['id']

def add_songs_to_spotify_playlist() -> None:
    """
    We get the song info, create a playlist, and then add the songs to the playlist.
    """
    get_playlist_items()

    uris = [info["spotify_uri"]for song, info in song_info.items()]

    playlist_id = create_playlist()

    request_data = json.dumps(uris)

    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
        playlist_id)

    print("Finalizing...")

    response = requests.post(
        query,
        data=request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )
    print(response)


