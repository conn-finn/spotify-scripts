# Spotify Fifteen From Fifteen:

## Description:
Automatically updates a public playlist weekly with 15 random songs from 15 different artists, selected from another playlist (which is private and populated with music already), removing the songs currently in the playlist. Python script Utilizes the [Spotipy](https://spotipy.readthedocs.io/en/latest/) library to interact with Spotify's API. 

## Features:
 * 15 different songs from 15 different artists (no more than 1 per artist)
 * updated weekly
 * picked from another playlist of songs already populated with songs
 * Utilizes Windows Scheduler
 * Updates only when 15 songs are in the pre-populated playlist
   * how to deal with less than 15 songs? - currently doesn't update at all
 * maybe display stats somehow in playlist comment in the future? most listened to by me or something?
 
## Status
- [x] create git repository/README
- [x] remove old weekly songs from playlist
- [x] remove new songs from source playlist
- [x] add new songs to weekly playlist
- [x] add checks
- [x] show when playlist was updated
- [x] choose a few songs from pool playlist that have been there the longest

# Judging Tracks By Their Album Cover:

## Description:
Just creates a cool little html page based on a playlist of songs which i think have cool album covers. Python script Utilizes the [Spotipy](https://spotipy.readthedocs.io/en/latest/) library to interact with Spotify's API.

## Features:
An Html Page with the following for multiple albums:
 * Album art
 * Band Name
 * Album Name
 * Previewable track from album

## Status
- [x] creates website of cover art
- [x] give artist and album name
- [x] give a preview of a song from the album
- [ ] clean up code a bit/rename repository and files to reflect additions
- [ ] give additional info, maybe webscraped from some album review site
- [ ] additional features like album descriptions, voting, etc.