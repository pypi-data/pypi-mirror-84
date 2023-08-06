import matplotlib.pyplot as plt
import numpy as np

def scambia(im, pos):
    if pos == 0:
        new_im = np.dstack((im[:, :, 2], im[:, :, 1], im[:, :, 0]))
    elif pos == 1:
        new_im = np.dstack((im[:, :, 0], im[:, :, 2], im[:, :, 1]))
    else:
        new_im = im

    return new_im


if __name__ == "__main__":
    im_test = plt.imread('flower.jpg')
    new_im = scambia(im_test, 0)
    plt.imshow(new_im)
    plt.show()
