import random
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
PLAYLIST_SIZE = 15
 
token = util.prompt_for_user_token(username, scope, client_id = spotipy_client_id, client_secret = spotipy_client_secret, redirect_uri = spotipy_redirect_url)

if token:
    spotify = spotipy.Spotify(auth = token)
    spotify.trace = False

    # remove old tracks from playlist
    response = spotify.user_playlist(username, playlist_id, fields = 'tracks, next')
    tracksToRemove = []
    for i, item in enumerate(response['tracks']['items']):
        track = {
            "positions": [i],
            "uri": item['track']['id']
        }
        tracksToRemove.append(track)
    spotify.user_playlist_remove_specific_occurrences_of_tracks(username, playlist_id, tracksToRemove)

    # find n songs from source playlist
    response = spotify.user_playlist(username, source_playlist_id, fields = 'tracks ,next')
    newTracks = []
    newArtists = []
    while len(newArtists) < PLAYLIST_SIZE:
        ran = random.randrange(len(response['tracks']['items'])-1)
        item = response['tracks']['items'][ran]
        track = {
            "positions": [ran],
            "uri": item['track']['id']
        }
        # retrieve main artist id
        artist = item['track']['artists'][0]['id']
        if artist not in newArtists:
            newArtists.append(artist)
            newTracks.append(track)

    # remove these songs from source playlist
    spotify.user_playlist_remove_specific_occurrences_of_tracks(username, source_playlist_id, newTracks)

    # add new songs from source to weekly playlist
    newTrackIds = (track["uri"] for track in newTracks)
    spotify.user_playlist_add_tracks(username, playlist_id, newTrackIds)


else:
    print("Cannot get token for ", username)
