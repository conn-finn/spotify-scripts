import spotipy
import spotipy.util as util

class AlbumInfo:
    def __init__(self, name, artist, coverUrl, genres):
        self.name = name
        self.artist = artist
        self.coverUrl = coverUrl
        self.genres = genres
         
        
class SpotifyInfo:

    spotify = None

    def __init__(self, username, scope, spotipy_client_id, spotipy_client_secret, spotipy_redirect_url):
        self.username = username
        self.scope = scope
        self.spotipy_client_id = spotipy_client_id
        self.spotipy_client_secret = spotipy_client_secret
        self.spotipy_redirect_url = spotipy_redirect_url
        self.valid = False

    def validate(self):
        token = util.prompt_for_user_token(self.username, self.scope, client_id = self.spotipy_client_id, client_secret = self.spotipy_client_secret, redirect_uri = self.spotipy_redirect_url)
        if not token:
            print("Cannot get token for ", self.username, "\nquitting")
            self.valid = False
        else:
            self.spotify = spotipy.Spotify(auth = token)
            self.valid = True
        return token

    # getPlaylistAlbumInfo helper methods are hidden 
    def __getPlaylistTracks(self, playlist_id): #api call to get tracks from playlist
        return self.spotify.user_playlist(self.username, playlist_id, fields = 'tracks ,next')['tracks']['items']

    # api call to get the album's genres (if there are none, just get artist genres)
    def __getAlbumGenres(self, album_id, artist_id):
        genres = self.spotify.album(album_id)['genres']
        if len(genres) < 1: genres = self.spotify.artist(artist_id)['genres']
        return genres

    #create albuminfo object from a track object
    def __getAlbumInfoFromTrack(self, trackObj): 
        track = trackObj['track']
        cover = track['album']['images'][0]['url']
        artist = track['album']['artists'][0]['name']
        album = track['album']['name']
        artist_id = track['album']['artists'][0]['id']
        album_id = track['album']['id']
        genres = self.__getAlbumGenres(album_id, artist_id)
        return AlbumInfo(album, artist, cover, genres)

    # for every genre the album "has", add to the list in the dictionary associated with that genre
    def __addAlbumToAllGenres(self, album, albumDict): 
        for genre in album.genres:
            if not albumDict[genre]: albumDict[genre] = [album]
            else: albumDict[genre].append(album)


    #returns a list of albumInfo objects
    def getPlaylistAlbumInfoList(self, playlist_id):
        tracks = self.__getPlaylistTracks(playlist_id)
        if len(tracks) < 1:
            print("No songs in playlist...\nquitting")
            return []
            
        albums = []
        for trackObj in tracks:
            if trackObj['is_local']: continue # ignore local files
            album = self.__getAlbumInfoFromTrack(trackObj)
            albums.append(album)

        if len(albums) < 1: print("Unable to get album art....\nquitting")
        return albums

    # returns a dictionary of albumInfo objects with genres as the keys
    def getPlaylistAlbumInfoDictionary(self, playlist_id):
        tracks = self.__getPlaylistTracks(playlist_id)
        if len(tracks) < 1: 
            print("No songs in playlist...\nquitting")
            return {}

        albums = {}
        for trackObj in tracks:
            if trackObj['is_local']: continue # ignore local files
            album = self.__getAlbumInfoFromTrack(trackObj)
            self.__addAlbumToAllGenres(album, albums)
        
        if len(albums) < 1: print("Unable to get album art....\nquitting")
        return albums 
