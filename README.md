# spotify-fifteen-from-fifteen

## Description:
Automatically updates a public playlist weekly with 15 random songs from 15 different artists, selected from another playlist (which is private and populated with music already), removing the songs currently in the playlist. Python script Utilizes the [Spotipy](https://spotipy.readthedocs.io/en/latest/) library to interact with Spotify's API. 

## Features:
 * 15 different songs from 15 different artists (no more than 1 per artist)
 * updated weekly
 * picked from another playlist of songs already populated with songs
 * Utilizes Windows Scheduler
 * Updates only when 15 songs are in the pre-populated playlist
   * how to deal with less than 15 songs? pick from another playlist or don't update at all?
 * maybe display stats somehow in playlist comment? most listened to by me or something?
 
## Status
* [x] create git repository/README
* [x] remove old weekly songs from playlist
