# -*- coding: utf-8 -*-

"""
euterpe.track
~~~~~~~~~~~~~

This module contains the basic `track` class for storing raw signal, 
spectrum, feature series, and basic info, also wrapping funcs from rs
"""

import os
import time
import json
import sys

import numpy as np
import pandas as pd

import librosa as rs
import librosa.feature as ft
import librosa.display as dp
import librosa.segment as sg

from euterpe.utils import gen_attr_dict


# GLOBAL_VARIABLES


class track(object):
    """Base class for track/seciton-wise analysis

    Data pack of raw time series, basic track and stamp information,
    derived features, feature generating methods, and plotting methods

    Attributes defined in groups with prefix '_' for encapsulation, for external
    uses, only through __init__ when constructing or @property, restrictions 
    for different groups:
    - basic info: 
        can be defined in __init__ and by external values
    - stamps: 
        can be defined in __init__ and by external values
        only after basic tag set is assigned
    - raw time series and sr: 
        can only be defined in __init__ and by self.load()
        after basic and stamp tag sets are assigned
        for external uses, read-only
    - features:
        PENDING
    """


    basic_tags = ['artist', 'album', 'name'] 
    stamp_tags = ['offset', 'duration']
    rawts_tags = ['y', 'sr']
    
    ad_basic_tags = gen_attr_dict(basic_tags)
    ad_stamp_tags = gen_attr_dict(stamp_tags)
    ad_rawts_tags = gen_attr_dict(rawts_tags)

    __slots__ = (ad_basic_tags.values()
              +  ad_stamp_tags.values()
              +  ad_rawts_tags.values())
    # + ... # visualize class structure
    # list of strings


    def __init__(self, **kwargs):
        """Check input and fill slots (by order)"""
        
        for tag in track.basic_tags:
            value = kwargs[tag] if tag in kwargs else None
            setattr(self, track.ad_basic_tags[tag], value)

        # assign stamp tags
        if all([
            getattr(self, track.ad_basic_tags[tag]) != None
            for tag in track.basic_tags
        ]): # check if all basic tags are assigned
            for tag in track.stamp_tags:
                value = kwargs[tag] if tag in kwargs else None
                setattr(self, track.ad_stamp_tags[tag], value)
        
        elif any([tag in kwargs for tag in track.stamp_tags]):
            raise(RuntimeError("Basic attrs required for assigning stamp attrs"))

        # assign raw time series
        if all([
            getattr(self, track.ad_basic_tags[tag]) != None
            for tag in track.basic_tags
        ]) and all([
            getattr(self, track.ad_stamp_tags[tag]) != None
            for tag in track.stamp_tags
            # Note that in default settings, duration is None
            # Only allow initiating (y, sr) when having complete
            # information on (offset, duration)
        ]):
            for tag in track.rawts_tags:
                value = kwargs[tag] if tag in kwargs else None
                setattr(self, track.ad_rawts_tags[tag], value)
        
        elif any([tag in kwargs for tag in track.rawts_tags]):
            raise(RuntimeError("Basic and Stamp attrs required for assigning ts attrs"))            

        # TODO: assign features
        # TODO: assign spectrum matrixes


    def load(self, db_path = '../data-raw/tracks/', 
             file_type = 'mp3'):
    
        if all([
            getattr(self, track.ad_basic_tags[tag]) != None
            for tag in track.basic_tags
        ]): # available for basic
            file_path = (db_path + self._artist + '/' + self._album + '/'
                         + self._name + '.' + file_type)

            # assign basic stamps, duration default is None 
            if self._offset == None: self._offset = 0.0
            
            vd = dict(zip(track.ad_rawts_tags.values(), 
                          rs.load(file_path, 
                                  offset = self._offset,
                                  duration = self._duration)))
            # value dictionary for attributes
            # key: attr names with '_', value: value to assign
            
        else:
            raise(RuntimeError("Basic attrs not assigned"))

        for key, value in vd.items():
            setattr(self, key, value)
            print("Attr assigned: {}".format(key))
        
        self._duration = round(len(self._y)/float(self._sr), 2)
        print("Attr assigned: _duration")

        return None


    def basic_info(self):
        report_tags = track.basic_tags + track.stamp_tags
        ad_report_tags = gen_attr_dict(report_tags)

        if all([
            getattr(self, ad_report_tags[tag]) != None
            for tag in report_tags
        ]):
            print("Artist: {}, "
                "Album: {}, "
                "Track Name: {},"
                "Offset: {},"
                "Duration: {}".format(
                    self._artist, 
                    self._album, 
                    self._name,
                    self._offset,
                    self._duration
                ))
        else:
            raise(RuntimeError("Some attrs are missing."))

        return None


    @property
    def artist(self): return self._artist
    @artist.setter
    def artist(self, value): self._artist = value

    @property
    def album(self): return self._album
    @album.setter
    def album(self, value): self._album = value
    
    @property
    def name(self): return self._name
    @name.setter
    def name(self, value): self._name = value
    
    @property
    def offset(self): return self._offset
    @offset.setter
    def offset(self, value): self._offset = value
    
    @property
    def duration(self): return self._duration
    @duration.setter
    def duration(self, value): self._duration = value
    
    @property
    def y(self): return self._y
    @y.setter
    def y(self, value): self._y = value

    @property
    def sr(self): return self._sr
    @sr.setter
    def sr(self, value): self._sr = value


    def __str__(self):
        raise(NotImplementedError)

    def __repr__(self):
        # TODO: should be used for updating the database
        raise(NotImplementedError)
        

    # property setters from external information
    # generate functions from internal wrapped functions