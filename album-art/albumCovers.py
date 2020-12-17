import numpy as np
import torch
from torchvision import datasets, transforms, models
import spotipy
import spotipy.util as util
from PIL import Image
import urllib

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from judgingTracksByAlbumCover import albumInfo, validate, handleResponse
from personalSpotifyInfo import playlists, client_id, client_secret, redirect_url, user, data_path, album_cover_data_path
sys.path.insert(0, data_path)

#Use GPU if available
dev = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def saveAlbumInfo(playlists, spotify, username):
    playlistAlbumInfo = []
    for playlist in playlists:
        pid = playlist["id"]
        response = spotify.user_playlist(username, pid, fields = 'tracks ,next')
        albumInfoList = handleResponse(response)
        playlistAlbumInfo.append(albumInfoList)
        print(f'saved {saveImages(playlist["name"], albumInfoList, album_cover_data_path)} images.')
    return np.array(playlistAlbumInfo)

# saves images, returns the number of album covers saved (does not save duplicates)
def saveImages(playlistName, albumInfo, data_dir): 
    counter = 0
    playlistPath = f'{data_dir}/{playlistName}'
    if not os.path.exists(playlistPath):
        os.makedirs(playlistPath)

    for album in albumInfo:
        filename = f'{album.coverUrl.split("/")[-1]}.png'
        full_name = f'{playlistPath}/{filename}'
        urllib.request.urlretrieve(album.coverUrl, full_name)
        counter += 1
    return counter


def load_split_train_test(album_covers_folder, valid_size=0.2, batch_size=64):
    train_data = datasets.ImageFolder(album_covers_folder, transform=transforms.Compose([transforms.Resize((640, 640)), transforms.ToTensor()]))
    test_data = datasets.ImageFolder(album_covers_folder, transform=transforms.Compose([transforms.Resize((640, 640)), transforms.ToTensor()]))
    num_train = len(train_data)
    indices = list(range(num_train))
    split = int(np.floor(valid_size * num_train))
    np.random.shuffle(indices)

    from torch.utils.data.sampler import SubsetRandomSampler
    train_idx, test_idx = indices[split:], indices[:split]
    train_sampler = SubsetRandomSampler(train_idx)
    test_sampler = SubsetRandomSampler(test_idx)
    trainloader = torch.utils.data.DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)
    testloader = torch.utils.data.DataLoader(test_data, sampler=test_sampler, batch_size=batch_size)
    return trainloader, testloader


def getInfo():
    username = user
    scope = 'playlist-modify-public playlist-modify-private'
    token = validate(username, scope, client_id, client_secret, redirect_url)
    spotify = spotipy.Spotify(auth = token)
    spotify.trace = False
    
    # playlistAlbumInfo = saveAlbumInfo(playlists, spotify, username)

    trainloader, testloader = load_split_train_test(album_cover_data_path)
    return trainloader, testloader

getInfo()