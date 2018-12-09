# -*- coding: utf-8 -*-

"""Tests for euterpe.track.track

TODO: pytest framework required implementation
"""

import os
import copy
import pytest
import numpy as np

from euterpe.track import track

example1 = {
    'artist' : 'Frank Ocean',
    'album' : 'Endless',
    'name' : 'UNITY'
}

example21 = copy.deepcopy(example1)
example21.update({
    'offset' : 0.0, 
    'duration' : None
})

example22 = {
    'artist' : 'Frank Ocean',
    'album' : 'Endless',
    'name' : None,
    'offset' : 0.0,
    'duration' : None
}

example31 = copy.deepcopy(example21)
example31.update({
    'sr' : 22050,
    'y' : np.array([1,2,3,4,5])
})

t1 = track(**example1)

t21 = track(**example21)
t22 = track(**example22)
# RuntimeError: name none, can't assign stamp tags

t3 = track(**example31) 
# RuntimeError: no specified duration, 