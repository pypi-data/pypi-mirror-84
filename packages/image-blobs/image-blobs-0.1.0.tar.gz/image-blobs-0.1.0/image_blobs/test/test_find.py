
import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

from ..util import make_image
from .. import find_blobs

def gauss1(dtype=None):
    '1x guassians'
    shape = (100, 200)
    Fs = [
        (100, 50, 20, 10, 2.5, 1),
    ]
    return make_image(shape, Fs, dtype=dtype)

def gauss2(dtype=None):
    '2x guassians'
    shape = (100, 200)
    Fs = [
        (100, 50, 20, 10, 2.5, 1),
        (150, 50, 10, 20, 5, 2),
    ]
    return make_image(shape, Fs, dtype=dtype)

def gauss4(dtype=None):
    shape = (100, 200) # 200x100
    Fs = [
        (100, 50, 4, 4, 2.5, 1),
        ( 40, 25, 4, 4, 3, 1),
        (160, 25, 4, 4, 4, 1),
        (150, 50, 5, 3, 5, 2),
    ]
    return make_image(shape, Fs, dtype=dtype)

class TestFind(unittest.TestCase):
    def test_zeros(self):
        'pathalogical case'
        img = np.zeros((100, 100), dtype='u1')
        B = find_blobs(img)
        self.assertEqual(len(B), 0)

    def test_noise(self):
        'realistic empty frame'
        img = (np.abs(np.random.randn(100,100))*5).astype('u1')
        B = find_blobs(img)
        self.assertEqual(len(B), 0)

    def test_single(self):
        img = gauss1('u1')
        B = find_blobs(img)
        B.sort(order='idx')

        assert_array_almost_equal(B['X'], [100], decimal=3)
        assert_array_almost_equal(B['Y'], [50],  decimal=3)
        assert_array_almost_equal(B['W'], [20],  decimal=1)
        assert_array_almost_equal(B['H'], [10],  decimal=1)
        assert_array_almost_equal(B['A'], [255], decimal=0)

    def test_four(self):
        img = gauss4('u1')
        B = find_blobs(img)
        B.sort(order='idx')

        assert_array_almost_equal(B['X'], [160.,  40., 100., 150.], decimal=3)
        assert_array_almost_equal(B['Y'], [ 25.,  25.,  50.,  50.], decimal=3)
        assert_array_almost_equal(B['W'], [  4.,   4.,   4.,   5.], decimal=1)
        assert_array_almost_equal(B['H'], [  4.,   4.,   4.,   3.], decimal=1)
        assert_array_almost_equal(B['A'], [204., 153., 128., 255.], decimal=0)
