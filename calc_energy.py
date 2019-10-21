import numpy as np
from skimage.io import imread
from skimage.color import rgb2gray
from scipy.ndimage import correlate

def calc_energy(img):
    if len(img.shape) == 3:
        img = rgb2gray(img)
    
    hH = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ])
    vH = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    return np.abs(correlate(img, hH)) + np.abs(correlate(img, vH))

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    img_path = 'path/to/img'
    img = imread(img_path)
    plt.imshow(img)
    plt.show()

    e1 = calc_energy(img)
    plt.imshow(e1)
    plt.show()
