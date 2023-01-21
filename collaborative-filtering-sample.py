import requests
import json

# Replace with your Spotify API client ID and secret
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

# Replace with your and your friends' Spotify usernames
my_username = "YOUR_USERNAME"
friend_usernames = ['YOUR_FRIEND_USERNAME_0', 'YOUR_FRIEND_USERNAME_1',...]

# Get an access token
auth_response = requests.post("https://accounts.spotify.com/api/token",
    data={
        "grant_type": "client_credentials"
    },
    auth=(client_id, client_secret)
)

access_token = auth_response.json()["access_token"]

def get_playlist_tracks(username=my_username):
    # Get 20 of the user's public playlists
    playlists_response = requests.get(f"https://api.spotify.com/v1/users/{username}/playlists/",#?limit=50",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    playlists = playlists_response.json()["items"]
    playlist_tracks = {}

    # Iterate through each playlist to find tracks
    for playlist in playlists:
        u = playlist["uri"]
        playlist_tracks[u] = []
        
        # Get the tracks in the playlist
        tracks_response = requests.get(playlist["tracks"]["href"],
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        tracks = tracks_response.json()["items"]
        
        # Store the URI of each track
        for track in tracks:
            if u is not None and track is not None and track["track"] is not None:
                playlist_tracks[u].append(track["track"]["uri"])

    return playlist_tracks

my_playlist_tracks = get_playlist_tracks()

# Basic collaborative filtering between you and your friends
for friend_username in friend_usernames:
    try:
        max_overlap = 0
        p_overlap = ''
        m_overlap = ''
        new_playlist_tracks = get_playlist_tracks(username=friend_username)
        for friend_p in new_playlist_tracks.keys():
            for my_p in my_playlist_tracks.keys():
                tmp_counter = 0
                for s in new_playlist_tracks[friend_p]:
                    if s in my_playlist_tracks[my_p]:
                        tmp_counter += 1
            if tmp_counter > max_overlap:
                max_overlap = tmp_counter
                p_overlap = friend_p
                m_overlap = my_p
        if max_overlap > 0:
            print('check out '+p_overlap+' ('+str(max_overlap)+' songs overlap with my '+m_overlap+'): user '+friend_username)
    except:
        pass
    

