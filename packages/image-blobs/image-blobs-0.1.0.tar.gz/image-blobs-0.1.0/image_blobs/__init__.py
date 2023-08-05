
import numpy as np
import scipy.ndimage as ndi
from scipy.optimize import least_squares

from . import util

__all__ = (
    'find_blobs',
)

def _error(F, Xs, Ys, I):
    return (util.gauss2d(F,Xs,Ys)-I).flatten()

def refine_feature(img, F):
    '''Refine a feature w/ gaussian fit
    '''

    X, Y, W, H, A, idx = F

    # extract sub-image with feature
    X0 = int(np.floor(X - W/2))
    X1 = int(np.ceil (X + W/2))
    Y0 = int(np.floor(Y - H/2))
    Y1 = int(np.ceil (Y + H/2))

    X0 = np.clip(X0, 0, img.shape[1])
    X1 = np.clip(X1, 0, img.shape[1])
    Y0 = np.clip(Y0, 0, img.shape[0])
    Y1 = np.clip(Y1, 0, img.shape[0])

    I = img[Y0:Y1, X0:X1]

    if I.size==0:
        raise ValueError("Empty feature: %s BB:%s"%(F, (X0, X1, Y0, Y1)))

    Ys, Xs = np.indices(I.shape)

    # fit parameters (offset, X, Y, W, H, A)
    initial = (0, X-X0, Y-Y0, W, H, A)
    # bounds
    lower = (0,     0,     0,     1,     1,     1)
    upper = (A, X1-X0, Y1-Y0, W*1.1, H*1.0, A*1.1)

    try:
        fit = least_squares(_error, initial, bounds=(lower, upper), args=(Xs, Ys, I))
    except ValueError:
        # initial not in bounds?
        raise

    O, X, Y, W, H, A = fit.x
    return np.asarray( (X+X0, Y+Y0, W, H, A, idx), dtype=util.features)


def find_blobs(img,
               bg=None,
               min_size=None,
               limit=None,
               smear=2.0,
               refine=True,
               debug=None):
    """Find discrete non-overlapping guassian blobs in a gray scale image with uniform background

    Returns an array of feature positions, widths, and amplitudes

    Parameters
    ----------

    img : 2x ndarray
        Image in HxW order
    bg : int, optional
        Background threshold.  pixel value.
    min_size : float, optional
        Minimum feature size in number of pixels.
    limit : int, optional
        Consider only N largest features.
    smear : float, optional
        Radius (in pixels) of gaussian smear prior to feature detection.
    refine : bool, optional
        If true, try to refine each blob with a 2d gaussian fit.

    Examples
    --------

    Process with default configuration and plot blob center points
    with 3 sigma error bars (requires matplotlib).

    >>> img = imread('blah.tiff')
    >>> B = blobs.find_blobs(img)
    >>> blobs.util.show_features(img, B, sigma=3.0)
    """
    assert img.ndim==2, "Only 2-d (gray) image supported"

    if debug==1:
        util.showimg(img, 'input image')

    W = img

    # smear to improve connectivity prior to labeling.
    if smear is not None:
        W = ndi.gaussian_filter(W, smear)
    if debug==2:
        util.showimg(W, 'smeared image')

    if bg is None:
        bg = util.guess_background(W)

    # background threshold cutoff
    W = W>bg
    if debug==3:
        util.showimg(W, 'cut-off')

    # feature labeling
    L, N = ndi.label(W)

    del W # no longer needed

    # all features except background (0)
    Fs = range(1, N+1)

    # sort by decreasing feature size in pixels
    sums = [(F, (L==F).sum()) for F in Fs]
    sums.sort(key=lambda p:p[1], reverse=True)

    # discard small features
    if min_size is not None:
        sums = [(F,C) for F,C in sums if C>=min_size]
    if limit is not None:
        sums = sums[:limit]

    Fs = [F for F,C in sums]

    blobs = np.ndarray(len(Fs), dtype=util.features)

    CoM = ndi.center_of_mass(img, L, Fs)
    blobs['A'] = ndi.maximum(img, L, Fs)

    for i in range(len(Fs)):
        R = blobs[i]
        R['idx'] = Fs[i]
        R['Y'], R['X'] = CoM[i]
        Xs, Ys = np.where(L==Fs[i])

        # start with feature bounding box
        R['H'], R['W'] = Xs.max()-Xs.min(), Ys.max()-Ys.min()

    if debug==5:
        util.show_features(img, blobs, 'Raw features')

    if refine:
        for i in range(len(Fs)):
            blobs[i] = refine_feature(img, blobs[i])

    if debug==7:
        util.show_features(img, blobs, 'Refined features')

    return blobs
