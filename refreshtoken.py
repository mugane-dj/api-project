import json
import requests
from secrets import refresh_token, base_64

class Refresh_token:

    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refresh(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(
            query,
            data={
                "grant_type":"refresh_token",
                "refresh_token":refresh_token
            },
            headers={
                    "Authorization": "Basic " + base_64
                }
        )
        return response.json()

if __name__=='__main__':
    r = Refresh_token()
    r.refresh()




