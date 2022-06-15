import json, os
import requests
from dotenv import load_dotenv
load_dotenv()

refresh_token = os.getenv("refresh_token")
base_64 = os.getenv("base_64")

def refresh() -> str:
    """
    It takes the refresh token and sends it to Spotify's API to get a new access token
    :return: The access token is being returned.
    """
    query = "https://accounts.spotify.com/api/token"
    response = requests.post(
        query,
        data={
            "grant_type":"refresh_token",
            "refresh_token":refresh_token
        },
        headers={
                "Authorization": "Basic " + base_64})
    response_json = response.json()
    return response_json['access_token']

if __name__ == "__main__":
    refresh()


