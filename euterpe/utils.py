# -*- coding: utf-8 -*-

import os
import numpy as np


def gen_attr_dict(l):
    tuples = zip(l, ['_' + e for e in l])
    return dict(tuples)


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
            names = clean_dir(track_path)
            
            for name in names:
                name = name.split('.')[0]
                tracklist.append([artist, album, name])
                
    return tracklist


def tracklist_todict(tracklist, fields = ['artist', 'album', 'name']):
    trackdict = [dict(zip(fields, track)) for track in tracklist]
    return trackdict


def gen_trackdict(db_path, fields = ['artist', 'album', 'name']):
    tracklist = gen_tracklist(db_path)
    trackdict = tracklist_todict(tracklist, fields)
    return trackdict
