# Spotify Scripts

## Album Cover AI

### Description:
Utilizes the [PyTorch](https://pytorch.org/) library to analyze the album covers from a number of personal spotify playlists which were obtained with the [Spotipy](https://spotipy.readthedocs.io/en/latest/) library to interact with Spotify's API. These album covers were sorted by genre and then used to train a convolutional Neural Network so that it can attempt to classify a album's genre based on the album cover alone. It is somewhat of an experiment to see how different are the album covers in seperate genres.

## Spotify Fifteen From Fifteen:

### Description:
Automatically updates a public playlist weekly with 15 random songs from 15 different artists, selected from another playlist (which is private and populated with music already), removing the songs currently in the playlist. Python script Utilizes the [Spotipy](https://spotipy.readthedocs.io/en/latest/) library to interact with Spotify's API. 

### Status:
- [x] save album covers from playlists based on genre
- [x] train CNN on album covers, using genre as desired output


### Features:
 * 15 different songs from 15 different artists (no more than 1 per artist)
 * updated weekly
 * picked from another playlist of songs already populated with songs
 * Utilizes Windows Scheduler
 * Updates only when 15 songs are in the pre-populated playlist
   * how to deal with less than 15 songs? - currently doesn't update at all
 * maybe display stats somehow in playlist comment in the future? most listened to by me or something?
 
### Status:
- [x] create git repository/README
- [x] remove old weekly songs from playlist
- [x] remove new songs from source playlist
- [x] add new songs to weekly playlist
- [x] add checks
- [x] show when playlist was updated
- [x] prevent starvation of older songs

## Judging Tracks By Their Album Cover:

### Description:
Just creates a cool little html page based on a playlist of songs which i think have cool album covers. Python script Utilizes the [Spotipy](https://spotipy.readthedocs.io/en/latest/) library to interact with Spotify's API.

### Features:
An Html Page with the following for multiple albums:
 * Album art
 * Band Name
 * Album Name
 * Previewable track from album

### Status:
- [x] creates website of cover art
- [x] give artist and album name
- [x] give a preview of a song from the album
- [ ] give additional info, maybe webscraped from some album review site
- [ ] additional features like album descriptions, voting, etc.
- [ ] preview of music video on hover or something

## Judging Tracks By Their Album Cover Part 2:

### Description:
Updates a web page with a number of album covers, users can vote between the album covers on the next song to be played. After a song has been chosen, the page updates with new album covers and the song will be added to a queue (or is added to another playlist which deletes the song being played currently). Will choose a song randomly if a tie occurs, or no one votes. Ideally would be an app. Python script Utilizes the [Spotipy](https://spotipy.readthedocs.io/en/latest/) library to interact with Spotify's API.

## Landmarks:
- [] start 

### Description: 
Very similar to "Judging Tracks By Their Album Cover". A Web page consisting of the songs from the landmarks playlist and a preview of the song as well as an image from the location they represent. Python script Utilizes the [Spotipy](https://spotipy.readthedocs.io/en/latest/) library to interact with Spotify's API.