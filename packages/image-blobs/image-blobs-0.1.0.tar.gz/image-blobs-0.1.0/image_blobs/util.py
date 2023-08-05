
import numpy as np

__all__ = (
    'features',
    'make_image',
    'show_features',
)

# scipy imread() returns images as HxW or HxWx3
# we maintain this coordinate system with Y and H referring to the outer-most dimension

features = np.dtype([
    ('X', 'f8'),
    ('Y', 'f8'),
    ('W', 'f8'),
    ('H', 'f8'),
    ('A', 'f8'),
    ('idx', 'u4'),
])

def gauss2d(F, Xs, Ys):
    '''Sample 2-d guassian at points Xs, Ys
    '''
    O, X, Y, W, H, A = F[:6]

    return O + A * np.exp((-(Xs-X)**2)/(2*W**2)) * np.exp((-(Ys-Y)**2)/(2*H**2))

def make_image(shape, Fs, dtype=None):
    '''Generate a test image with the given shape and guassian blobs.
    '''
    Fs = np.asarray(Fs, dtype=features)
    img = np.zeros(shape, dtype='f8')

    Ys, Xs = np.indices(img.shape)

    for F in Fs:
        img += gauss2d((0,)+tuple(F), Xs, Ys)

    if dtype is not None:
        dtype = np.dtype(dtype)
        img /= img.max()
        if dtype.kind in 'ui':
            img *= np.iinfo(dtype).max
        img = img.astype(dtype)

    return img

def guess_background(img):
    return np.asarray(np.median(img.flatten())*4.0, dtype=img.dtype)

def showimg(img, title=''):
    '''Shorthand for matplotlib.pyplot.imshow()
    '''
    import matplotlib.pyplot as plt
    plt.imshow(img)
    plt.title(title)
    plt.show()

def show_features(img, Fs, title='', sigma=1.0):
    '''Show image superimposed with blob position and size
    '''
    import matplotlib.pyplot as plt
    plt.imshow(img)
    plt.errorbar(Fs['X'], Fs['Y'], xerr=Fs['W']*0.5*sigma, yerr=Fs['H']*0.5*sigma, fmt='b+')
    plt.title(title)
    plt.show()
