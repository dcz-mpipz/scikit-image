import numpy as np
from numpy.testing import assert_equal, assert_array_equal, assert_raises

from skimage._shared.testing import assert_greater, test_parallel
from skimage.segmentation import felzenszwalb
from skimage import data

@test_parallel()
def test_grey():
    # very weak tests.
    img = np.zeros((20, 21))
    img[:10, 10:] = 0.2
    img[10:, :10] = 0.4
    img[10:, 10:] = 0.6
    seg = felzenszwalb(img, sigma=0)
    # we expect 4 segments:
    assert_equal(len(np.unique(seg)), 4)
    # that mostly respect the 4 regions:
    for i in range(4):
        hist = np.histogram(img[seg == i], bins=[0, 0.1, 0.3, 0.5, 1])[0]
        assert_greater(hist[i], 40)

def test_minsize():
    # single-channel:
    img = data.coins()[20:168,0:128]
    for min_size in np.arange(10, 100, 10):
        segments = felzenszwalb(img, min_size=min_size, sigma=3)
        counts = np.bincount(segments.ravel())
        # actually want to test greater or equal.
        assert_greater(counts.min() + 1, min_size)
    # multi-channel:
    coffee = data.coffee()[::4, ::4]
    for min_size in np.arange(10, 100, 10):
        segments = felzenszwalb(coffee, min_size=min_size, sigma=3)
        counts = np.bincount(segments.ravel())
        # actually want to test greater or equal.
        assert_greater(counts.min() + 1, min_size)

def test_3D():
    img = np.zeros((10, 10, 10))
    assert_raises(ValueError, felzenszwalb, img)

def test_color():
    # very weak tests.
    img = np.zeros((20, 21, 3))
    img[:10, :10, 0] = 1
    img[10:, :10, 1] = 1
    img[10:, 10:, 2] = 1
    seg = felzenszwalb(img, sigma=0)
    # we expect 4 segments:
    assert_equal(len(np.unique(seg)), 4)
    assert_array_equal(seg[:10, :10], 0)
    assert_array_equal(seg[10:, :10], 2)
    assert_array_equal(seg[:10, 10:], 1)
    assert_array_equal(seg[10:, 10:], 3)


def test_merging():
    # test region merging in the post-processing step
    img = np.array([[0, 0.3], [0.7, 1]])
    # With scale=0, only the post-processing is performed.
    seg = felzenszwalb(img, scale=0, sigma=0, min_size=2)
    # we expect 2 segments:
    assert_equal(len(np.unique(seg)), 2)
    assert_array_equal(seg[0, :], 0)
    assert_array_equal(seg[1, :], 1)


if __name__ == '__main__':
    from numpy import testing
    testing.run_module_suite()
