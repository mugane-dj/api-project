# api-project
After finishing learning fundamentals of python programming, I decided to push myself to do my first project using APIs.
Spotify finally came to Kenya and I was inspired by [@TheComeUpCode](https://github.com/TheComeUpCode) and [@EuanMorgan](https://github.com/EuanMorgan) to build a python automation script using the youtube's API and spotify's API.
Both these APIs have great documentation which provides code snippets for easy understaning and follow-up.

<hr />

### Libraries

 Libraries used in the script:

 1. Google-auth-oauth
 2. Youtube-dl
 3. Requests
 4. Googleapiclient
 5. JSON
 6. OS
 
<hr />

### Script snapshots
![](https://github.com/roguecode25/api-project/blob/714eba6882c6864cbdec3b1cdc26da4655c6964b/snapshots/playlist.png)
**Figure 1** - spotify playlist

![](https://github.com/roguecode25/api-project/blob/714eba6882c6864cbdec3b1cdc26da4655c6964b/snapshots/youtubesnapshot.png)
**Figure 2** - Youtube Playlist

![](https://github.com/roguecode25/api-project/blob/714eba6882c6864cbdec3b1cdc26da4655c6964b/snapshots/terminal2.png)
**Figure 3** - Output

<hr />

### Code Limitation
This script is unique to the playlist chosen. The playlist id is needed and one needs to indentify how the channel describes the title of the video to ensure that the split() method works to extract the song_name and artist for the song_info dict.