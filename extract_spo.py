import requests
import os
import itertools
from dotenv import load_dotenv
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

import pandas as pd
import numpy as np

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
scope = "user-read-playback-state user-read-currently-playing playlist-read-private playlist-read-collaborative user-follow-read user-read-recently-played user-top-read user-library-read"
token = util.prompt_for_user_token('animatroniccanister', scope, client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8888/callback')
spotify = spotipy.Spotify(auth=token)




# client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

# spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_playlist_tracks():
    playlists = spotify.user_playlists('animatroniccanister')
    tracks = []
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            userPlaylist = playlist['uri']
            playlistTracks = spotify.playlist_tracks(userPlaylist)
            trackItems = playlistTracks['items']
            for k in range(len(trackItems)):
                trackItem = trackItems[k]
                track = trackItem['track']
                tracks.append(track['name'])
        if playlists['next']:
            playlists = spotify.next(playlists)
        else:
            playlists = None
    return tracks


def get_specific_playlist_tracks(playlist_name):
    playlists = spotify.user_playlists('animatroniccanister')
    tracks = []
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if playlist['name'] == playlist_name:
                user_playlist = playlist['uri']
                playlist_tracks = spotify.playlist_tracks(user_playlist)
                track_items = playlist_tracks['items']  
                for i in range(len(track_items)):
                    track_item = track_items[i]
                    track = track_item['track']
                    tracks.append(track['name'])
                break
            else:
                continue
        if playlists['next']:
            playlists = spotify.next(playlists)
        else:
            playlists = None
    return tracks

def get_specific_playlist_genres(playlist_name):
    playlists = spotify.user_playlists('animatroniccanister')
    genres = []
    artists = []
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if playlist['name'] == playlist_name:
                user_playlist = playlist['uri']
                playlist_tracks = spotify.playlist_tracks(user_playlist)
                track_items = playlist_tracks['items']  
                for i in range(len(track_items)):
                    track_item = track_items[i]
                    track = track_item['track']
                    track_artists = track['artists'][0]['id']
                    artists.append(track_artists) 
                break
            else:
                continue
        if playlists['next']:
            playlists = spotify.next(playlists)
        else:
            playlists = None
        artist_info = spotify.artists(artists)
        artist_genres = [i['genres'] for i in artist_info['artists']]
        flattened_genres = list(itertools.chain(*artist_genres))
        genres = list(set(flattened_genres))
    return genres


def remove_none(none_list):
    new_list = []
    for val in none_list:
        if val != None:
            new_list.append(val)
    return new_list

def get_current_user():
    return spotify.current_user()


# MESSAGE FOR LATER: THE SPOTIFY API DOESN'T LET YOU GO OVER THE LIMIT FOR THIS COMMAND SO IT'S JUST GONNA BE STUCK AT 50 FOREVER
# DON'T TRY TO CHANGE THIS IT'S SUCH A WASTE OF TIME BRUH
def get_recently_played_songs():
    recently_played_songs = []
    recently_played = spotify.current_user_recently_played(limit=50)
    rp_items = recently_played['items']
    for i in range(len(rp_items)):
        rp_item = rp_items[i]
        track = rp_item['track']
        recently_played_songs.append(track['name'])
    return recently_played_songs

def get_recently_played_artists():
    recently_played_artists = []
    recently_played = spotify.current_user_recently_played(limit=50)
    rp_items = recently_played['items']
    for i in range(len(rp_items)):
        rp_item = rp_items[i]
        track = rp_item['track']
        artist = track['artists']
        recently_played_artists.append(artist[0]['name'])
    return recently_played_artists

def get_recently_played_songs_uri():
    recently_played_uri = []
    str_pref = 'spotify:track:'
    recently_played = spotify.current_user_recently_played(limit=50)
    rp_items = recently_played['items']
    for i in range(len(rp_items)):
        rp_item = rp_items[i]
        context = rp_item['track']
        # print(context['uri'])
        recently_played_uri.append(context['uri'])
    for idx, ele in enumerate(recently_played_uri):
        recently_played_uri[idx] = ele.replace(str_pref, '')
    return recently_played_uri

def get_played_at():
    recently_played_time = []
    recently_played = spotify.current_user_recently_played(limit=50)
    rp_items = recently_played['items']
    for i in range(len(rp_items)):
        rp_item = rp_items[i]
        recently_played_time.append(rp_item['played_at'])
    return recently_played_time

def get_recent_genres():
    recently_played = spotify.current_user_recently_played(limit=50)
    rp_items = recently_played['items']
    artists = []
    genres = []
    for i in range(len(rp_items)):
        rp_item = rp_items[i]
        track = rp_item['track']
        artist_id = track['artists'][0]['id']
        # print(artist_id)
        artists.append(artist_id)
    artist_info = spotify.artists(artists)
    artist_genres = [i['genres'] for i in artist_info['artists']]
    # FOR LATER: IF YOU DECIDE YOU WANT A LIST OF UNIQUE GENRES, UNCOMMENT THE BELOW CODE AND RETURN GENRES
    # OTHERWISE ADD THE GENRE LIST TO THE SONG DATAFRAME
    # flattened_genres = list(itertools.chain(*artist_genres))
    # genres = list(set(flattened_genres))
    return artist_genres


def get_saved_tracks():
    saved_tracks = []
    saved = spotify.current_user_saved_tracks(limit=50)
    saved_items = saved['items']
    j = 0
    for j in range(0,2):
        # print(saved['items'][0]['track']['name'])
        saved = spotify.next(saved)
        for i in range(len(saved_items)):
            saved_item = saved_items[i]
            track = saved_item['track']
            saved_tracks.append(track['name'])
        # print(saved['items'][0]['track']['name'])
        saved_items = saved['items']
    # return saved_tracks

def create_recently_played_df():
    song_name = get_recently_played_songs()
    song_artist = get_recently_played_artists()
    uris = get_recently_played_songs_uri()
    timestamp = get_played_at()
    # print(song_name)
    # print(song_artist)
    song_dict = {
        "song_name": song_name,
        "song_artist": song_artist,
        "uri": uris,
        "timestamp": timestamp
    }
    # print(song_dict)
    song_df = pd.DataFrame.from_dict(song_dict)
    song_df.columns = ['Name', 'Artist', 'ID', 'Timestamp']
    # print(len(song_df['Timestamp'].unique()))
    return song_df
    

    
print(create_recently_played_df())
# print(get_recent_genres())
