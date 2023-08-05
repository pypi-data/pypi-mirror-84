import matplotlib.pyplot as plt
import numpy as np
import media
import scambia


def test_media():
    # verifico la prima proprietà della media, ovvero che la somma degli scarti di ciascun valore di x è nulla
    # sum(xi-M)=0
    # carico immagine su cui fare il test
    im = plt.imread('immagini/flower.jpg')

    im_red = im[:, :, 0]
    im_green = im[:, :, 1]
    im_blue = im[:, :, 2]

    array_medie = media.get_media(im)

    # canale del rosso
    s_r = 0
    for i in im_red:
        for j in i:
            ss_r = j - array_medie[0]
            s_r = s_r + ss_r

    # canale del verde
    s_g = 0
    for i in im_green:
        for j in i:
            ss_g = j - array_medie[1]
            s_g = s_g + ss_g

    # canale del blu
    s_b = 0
    for i in im_blue:
        for j in i:
            ss_b = j - array_medie[2]
            s_b = s_b + ss_b

    assert (s_r > -0.01 and s_r < 0.01) and (s_g > -0.01 and s_g < 0.01) and \
           (s_b > -0.01 and s_b < 0.01), "la somma degli scarti non è 0"


def test_scambia():
    # carico l' immagine su cui fare il test
    im = plt.imread('immagini/flower.jpg')

    # verifico che scambiando due volte gli stessi canali l' immagine risultante è la stessa di quella di partenza
    for i in range(3):
        new_im = scambia.scambia(scambia.scambia(im, i), i)
        assert np.allclose(new_im, im), "scambiando due volte gli stessi canali le immagini non sono uguali"


