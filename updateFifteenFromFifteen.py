import pprint
import sys
from personalSpotifyInfo import *

import spotipy
import spotipy.util as util

username = user
playlist_id = playlist_id1
source_playlist_id = playlist_id2
scope = 'playlist-modify-public playlist-modify-private'
spotipy_client_id = client_id
spotipy_client_secret = client_secret
spotipy_redirect_url = redirect_url
 
token = util.prompt_for_user_token(username, scope, client_id = spotipy_client_id, client_secret = spotipy_client_secret, redirect_uri = spotipy_redirect_url)

if token:
    spotify = spotipy.Spotify(auth = token)
    spotify.trace = False

    response = spotify.user_playlist(username, playlist_id, fields = 'tracks,next')

    #remove old tracks from playlist
    tracksToRemove = []
    for i, item in enumerate(response['tracks']['items']):
        track = {
            "positions": [i],
            "uri": item['track']['id']
        }
        tracksToRemove.append(track)

    spotify.user_playlist_remove_specific_occurrences_of_tracks(username, playlist_id, tracksToRemove)


else:
    print("Cannot get token for ", username)
