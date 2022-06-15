# api-project
A python script that fetches songs from a youtube playlist and adds the songs to a spotify playlist

<hr />

### Credits
After finishing my python fundamentals course, I decided to create my first project using APIs. The API's selected for the project include Youtube's API and Spotify's API. Both these APIs have great documentation which makes it easy to gather code snippets and conduct follow-up. The project was inspired by [@TheComeUpCode](https://github.com/TheComeUpCode) and [@EuanMorgan](https://github.com/EuanMorgan).

<hr />

### Running the script
1. Gather credentials from youtube api [Link](https://console.cloud.google.com/apis).
2. Gather credentials from spotify api [Link](https://developer.spotify.com/dashboard/).
3. Fill in your spotify user id, spotify token, refresh token, base 64 string of client id and client secret accessed through Spotify's API and the youtube playliust id in a .env file. The playlist id is extracted as shown below;
![](https://github.com/roguecode25/api-project/blob/fa5b5f0d956b7293b04caead56cc8f1d42255308/snapshots/playlistid.png) 
**Figure 1 - Playlist Id**
    
    The highlighted object is the playlist Id.
4. Install requirements
    `pip install -r requirements.txt`
5. Run script
    `python main.py`

<hr />

### Snapshots
![](https://github.com/roguecode25/api-project/blob/fa5b5f0d956b7293b04caead56cc8f1d42255308/snapshots/playlist.png) 
**Figure 2 - Spotify Playlist**
[Link](https://open.spotify.com/playlist/7CfmVtlNIjVlybif7tEa82?si=8d6ec30a038a403d)

![](https://github.com/roguecode25/api-project/blob/fa5b5f0d956b7293b04caead56cc8f1d42255308/snapshots/youtubesnapshot.png) 
**Figure 3 - Youtube Playlist**
[Link](https://youtube.com/playlist?list=PLWa4R2I19VH6xvVHSISkIZk_wkg-i3tTb)

![](https://github.com/roguecode25/api-project/blob/fa5b5f0d956b7293b04caead56cc8f1d42255308/snapshots/terminal2.png) 
**Figure 4 - Output**
