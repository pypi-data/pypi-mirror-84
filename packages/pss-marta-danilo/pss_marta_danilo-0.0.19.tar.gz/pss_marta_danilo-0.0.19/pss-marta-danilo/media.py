import matplotlib.pyplot as plt
import numpy as np

def get_media (im):

    # canale del rosso
    im_red = im[:,:,0]
    # canale del verde
    im_green = im[:,:,1]
    # canale del blu
    im_blue = im[:,:,2]

    rc = np.shape(im)
    dim = rc[0] * rc[1]

    m_red = sum(im_red.sum(axis=0))/dim
    m_green = sum(im_green.sum(axis=0))/dim
    m_blue = sum(im_blue.sum(axis=0))/dim

    media = [m_red, m_green, m_blue]

    return media

if __name__ == "__main__":
    im_test = plt.imread('flower.jpg')
    array_medie = get_media(im_test)
    print("questo è l' array delle medie dell' immagine di test:")
    print(array_medie)
