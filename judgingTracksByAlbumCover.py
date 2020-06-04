import random
from datetime import datetime

from personalSpotifyInfo import album_art_playlist_id, client_id, client_secret, redirect_url, user

import spotipy
import spotipy.util as util


playlist_id = album_art_playlist_id

filename = "judgingTracksByTheirAlbumCover.html"
stylesheet = "stylesheet.css"


class albumInfo:

    def __init__(self, name, artist, coverUrl, previewUrl, previewName):
        self.name = name
        self.artist = artist
        self.coverUrl = coverUrl
        self.previewUrl = previewUrl
        self.previewName = previewName
        # preview based on track in source playlist ie not just a random song from the album

    def getId(self):
        return self.coverUrl.strip().split("image/")[1]

    def getCoverTag(self):
        return f'<div class="album-container"><img src="{self.coverUrl}"></div>'

    def getInfoTag(self):
        return f'<div class="album-info"><h2 class="artist-name">{self.artist}</h2><div class="border"></div><h2 class="album-name">{self.name}</h2></div>'

    def getPreviewTag(self): 
        return f'<div class="preview-container"><audio controls class="preview"><source src="{self.previewUrl}">klewtrklgnk</audio><h4 class="track-name">Preview Track: {self.previewName}</h4></div>'


def validate(username, scope, spotipy_client_id, spotipy_client_secret, spotipy_redirect_url):

    token = util.prompt_for_user_token(username, scope, client_id = spotipy_client_id, client_secret = spotipy_client_secret, redirect_uri = spotipy_redirect_url)
    if not token:
        print("Cannot get token for ", username, "\nquitting")
        quit()
    return token

#returns a list of albumInfo objects
def handleResponse(response):
    tracks = response['tracks']['items']
    if len(tracks) < 1:
        print("No songs in playlist...\nquitting")
        quit()

    albums = []
    for trackObj in tracks:
        track = trackObj['track']
        cover = track['album']['images'][0]['url']
        artist = track['album']['artists'][0]['name']
        album = track['album']['name']
        preview = track['preview_url']
        previewName = track['name']
        albums.append(albumInfo(album, artist, cover, preview, previewName))

    if len(albums) < 1:
        print("Unable to get album art....\nquitting")
        quit()
    return albums

def writeHTMLFile(filename, albums):
    with open(filename, 'r') as f:
        f.read()
    f = open(filename, 'w')

    boilerplateHTML = [f'<html><head><link rel="stylesheet" href="{stylesheet}"></head><body>', f'</body></html>']
    
    f.write(boilerplateHTML[0])
    f.write(f'<div id="content">')
    
    for album in albums:
        content = ""
        content += album.getCoverTag()
        content += album.getInfoTag()
        content += album.getPreviewTag()
        f.write(content)

    f.write("</div>")
    f.write(boilerplateHTML[1])
    f.close()

def main():
    username = user
    scope = 'playlist-modify-public playlist-modify-private'
    
    token = validate(username, scope, client_id, client_secret, redirect_url)

    spotify = spotipy.Spotify(auth = token)
    spotify.trace = False
    
    response = spotify.user_playlist(username, playlist_id, fields = 'tracks ,next')

    albumInfoList = handleResponse(response)
    writeHTMLFile(filename, albumInfoList)
    

main()