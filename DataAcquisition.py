import sys
import spotipy
import spotipy.util as util
import pandas as pd
from pymongo import MongoClient
import datetime

#RUN EVERY WEEK 8/23

today = str(datetime.date.today())
#today = "2017-09-01" #IF YOU MISSED A DAY STEP BACK
client = MongoClient()
db = client.SpotifyDB
genreCollection = db['TopGenres']
trackCollection = db['TopTracks']
document =  db.document
username = 'heyaaaaarnold'

scope = 'user-top-read'
genreList,tracksList = [],[]


def getArtists():
    print(sp.current_user_top_artists())
    topArtists = sp.current_user_top_artists(limit=40, time_range='short_term')
    print(topArtists)
    # print(sp.user_playlists(username))
    for artist in topArtists['items']:
        print()
        print(artist['name'])
        print("GENRES : ")
        for genre in artist['genres']:
            print(genre)
            genreList.append(genre)
            print()
            genreCollection.insert_one(
                {
                    "date":today,
                    "name":artist['name'],
                    "genre":genre
                }
            )

def getTracks():
    topTracks = sp.current_user_top_tracks(limit=40, time_range='short_term')
    print(topTracks)
    for songs in topTracks['items']:
        print()
        print(songs['name'])
        tracksList.append(songs['name'])

        trackCollection.insert_one(
            {
                "date":today,
                "track":songs['name']
            }
        )



if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print ("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(
    username,
    scope,
    client_id='c0568741538149a3a388a19fd2607641',
    client_secret='9411fcb24f7e4f6ea462cc9f7fb8761c',
    redirect_uri='http://www.google.com')

if token:


    print(username)
    sp = spotipy.Spotify(auth=token)
    #print(sp.current_user())
    getTracks()

    print('##############################')

    getArtists()
    """
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print
            print (playlist['name'])
            print ('  total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks)
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)
    """
else:
    print ("Can't get token for", username)
