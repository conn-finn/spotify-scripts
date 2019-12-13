import random
from datetime import datetime
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
MIN_SOURCE_PLAYLIST_SIZE = 20
RANDOM_THRESHOLD = 30
 
token = util.prompt_for_user_token(username, scope, client_id = spotipy_client_id, client_secret = spotipy_client_secret, redirect_uri = spotipy_redirect_url)

def main():
    if token:
        spotify = spotipy.Spotify(auth = token)
        spotify.trace = False

        # check if there are enough songs in our source playlist
        response = spotify.user_playlist(username, source_playlist_id, fields = 'tracks ,next')
        source_length = len(response['tracks']['items'])
        if source_length < MIN_SOURCE_PLAYLIST_SIZE:
            print("Not enough songs in source playlist")
            return
        
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
        # if source is big enough, pick songs randomly
        if source_length > RANDOM_THRESHOLD:
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
        else:
            for i, item in enumerate(response['tracks']['items']):
                track = {
                    "positions": [i],
                    "uri": item['track']['id']
                }
                # retrieve main artist id
                artist = item['track']['artists'][0]['id']
                if artist not in newArtists:
                    newArtists.append(artist)
                    newTracks.append(track)
                if len(newArtists) > 14:
                    break

        # remove these songs from source playlist
        spotify.user_playlist_remove_specific_occurrences_of_tracks(username, source_playlist_id, newTracks)

        # add new songs from source to weekly playlist
        newTrackIds = (track["uri"] for track in newTracks)
        spotify.user_playlist_add_tracks(username, playlist_id, newTrackIds)

        # add description to the weekly playlist
        currentTime = datetime.now()
        timeString = currentTime.strftime("Updated: %B %d, %Y")
        #currently cannot change description with spotipy so i'll just put the time in the title
        title = "Weekly Fifteen From Fifteen " + timeString
        spotify.user_playlist_change_details(username, playlist_id, title)

    else:
        print("Cannot get token for ", username)

if __name__ == '__main__':
    main()