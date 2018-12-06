# -*- coding: utf-8 -*-

import os
import numpy as np


def clean_dir(path, excludes = ['.DS_Store']):
    files = os.listdir(path)
    
    for exclude in excludes:
        if exclude in files:
            files.remove(exclude)
    
    return files


def gen_tracklist(db_path):
    tracklist = []
    
    artists = clean_dir(db_path)
    
    for artist in artists:
        artist_path = db_path + artist + '/'
        albums = clean_dir(artist_path)
        
        for album in albums:
            track_path = artist_path + album + '/'
            tracks = clean_dir(track_path)
            
            for track in tracks:
                track = track.split('.')[0]
                tracklist.append([artist, album, track])
                
    return tracklist


def tracklist_todict(tracklist, fields = ['artist', 'album', 'track']):
    trackdict = [dict(zip(fields, track)) for track in tracklist]
    return trackdict


def gen_trackdict(db_path, fields = ['artist', 'album', 'track']):
    tracklist = gen_tracklist(db_path)
    trackdict = tracklist_todict(tracklist, fields)
    return trackdict
