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

from _internal_utils import gen_attr_dict

# GLOBAL_VARIABLES

class track(object):
    """Base class for track/seciton-wise analysis

    TODO: Description required
    """

    # shared class attributes, specified for memory mgmt
    # attr names are track._X, can called in methods 
    # @property attached for external use as track.X
    basic_info = ['artist', 'album', 'name'] # catch basic info
    # TODO: onset and duration for rawts_info
    stamp_info = ['onset', 'duration']
    rawts_info = ['y', 'sr'] # catch output of rs.load()
    
    ad_basic_info = gen_attr_dict(basic_info)
    ad_stamp_info = gen_attr_dict(stamp_info)
    ad_rawts_info = gen_attr_dict(rawts_info)

    __slots__ = (ad_basic_info.values()
              +  ad_stamp_info.values()
              +  ad_rawts_info.values())
    # + ... # visualize class structure


    def __init__(self, **kwargs):
        """Constructor

        Check input and fill slots (by order)
        """
        
        # first check and fill basic info        
        # can also manually set using @property
        # will be checked when pulling y and sr
        for info in track.basic_info:
            value = kwargs[info] if info in kwargs else None
            setattr(self, track.ad_basic_info[info], value)

        # TODO: check the availability of basic_info first
        # can also be manually set using @property
        if all([
            getattr(self, track.ad_basic_info[info]) != None
            for info in track.basic_info
        ]):
            for info in track.stamp_info:
                value = kwargs[info] if info in kwargs else None
                setattr(self, track.ad_stamp_info[info], value)
        elif any([info in kwargs for info in track.stamp_info]):
            raise(RuntimeError("Basic attrs required for assigning stamp attrs"))

        # can only be passed in in init or self.load
        if all([
            getattr(self, track.ad_basic_info[info]) != None
            for info in track.basic_info
        ]) and all([
            getattr(self, track.ad_stamp_info[info]) != None
            for info in track.stamp_info
        ]):
            for info in track.rawts_info:
                value = kwargs[info] if info in kwargs else None
                setattr(self, track.ad_rawts_info[info], value)
        elif any([info in kwargs for info in track.stamp_info]):
            raise(RuntimeError("Basic and Stamp attrs required for assigning ts attrs"))            

        # TODO: features, functions, check availability before


    def load(self, db_path = '../data-raw/tracks/', 
             file_type = 'mp3'):


        # TDOO: implement onset and duration with the init framework

        if all([
            getattr(self, track.ad_basic_info[info]) != None
            for info in track.basic_info
        ]):
            file_path = (db_path + self.artist + '/' + self.album + '/'
                         + self.name + '.' + file_type)
            vd = dict(zip(track.ad_rawts_info.values(), 
                          rs.load(file_path)))
            # value dictionary for attributes

        else:
            raise(RuntimeError("Basic attrs not assigned"))

        for key, value in vd.items():
            setattr(self, key, value)
            print("Attr assigned sucessfully: {}".format(key))

        return None


    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        self._artist = value

    @property
    def album(self):
        return self._album

    @album.setter
    def album(self, value):
        self._album = value
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def y(self):
        return self._y

    @property
    def sr(self):
        return self._sr

    def __str__(self):
        raise(NotImplementedError)

    def __repr__(self):
        raise(NotImplementedError)

    # property setters from external information
    # generate functions from internal wrapped functions