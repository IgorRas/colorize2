import PySimpleGUI as sg
from PIL import Image
import shutil
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# wybranie obrazu do obróbki
def select_image():
    filename = sg.popup_get_file('file to open', no_window=True) # ścieżka do wybranego obrazu
    return filename


def save_image(filename):
    name = os.path.basename(filename)[:-4]
    img = Image.open(filename)
    path_to = sg.popup_get_folder('file to open', no_window=True)
    img.save(f'{path_to}/{name}.png', format='PNG')
    print('Saved')


def smooth(filename, num):
    img = cv2.imread(filename, 0)
    height = img.shape[0]
    width = img.shape[1]
    n_img = np.zeros([height, width])
    for i in range(height):
        for j in range(width):
            n_img[i][j] = img[i][j]/num
    fin_img = np.clip(n_img.round(), 0, 255)
    plt.imsave('copied/smooth.jpg', fin_img)


def mono1(filename):
    img = mpimg.imread(filename)
    lum_img = img[:, :, 0]
    plt.imshow(lum_img, cmap='Greys')
    plt.show()


def mono2(filename):
    img = mpimg.imread(filename)
    lum_img = img[:, :, 0]
    plt.imshow(lum_img, cmap='Greys_r')
    plt.show()


def spectrum(filename):
    img = mpimg.imread(filename)
    lum_img = img[:, :, 0]
    plt.imshow(lum_img, cmap='hsv')
    plt.show()


def rainbow(filename):
    img = mpimg.imread(filename)
    lum_img = img[:, :, 0]
    plt.imshow(lum_img, cmap='rainbow')
    plt.show()


def blackbody(filename):
    img = mpimg.imread(filename)
    lum_img = img[:, :, 0]
    plt.imshow(lum_img, cmap='autumn')
    plt.show()


def reds(filename):
    img = mpimg.imread(filename)
    lum_img = img[:, :, 0]
    plt.imshow(lum_img, cmap='Reds')
    plt.show()


def menus():
    sg.theme('LightGreen')
    sg.set_options(element_padding=(0, 0))

    # opcje menu
    menu_def = [['&File', ['&Open', 'Save']],
                ['&Modify', ['Smoothing']],
                ['Colorize', ['Monochrome(1)', 'Monochrome(2)', 'Spectrum', 'Rainbow', 'Blackbody', 'Iron']]]

    layout = [
        [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
        [sg.Output(expand_x=True, expand_y=True, size=(60, 5))]
    ]

    window = sg.Window("Colorize",
                       layout,
                       default_element_size=(12, 1),
                       default_button_element_size=(12, 1),
                       resizable=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            shutil.rmtree('copied')
            break
        print(event, values)
        # ------ Process menu choices ------ #
        if event == 'Open':
            filename = select_image()
        elif event == 'Save':
            save_image(filename)
        elif event == 'Smoothing':
            layout = [
                [sg.Text('Liczba:'), sg.InputText()],
                [sg.Submit()]
            ]
            n_window = sg.Window('Podaj dane', layout)
            event, values = n_window.read()
            n_window.close()
            smooth(filename, float(values[0]))
        elif event == 'Monochrome(1)':
            mono1(filename)
        elif event == 'Monochrome(2)':
            mono2(filename)
        elif event == 'Spectrum':
            spectrum(filename)
        elif event == 'Rainbow':
            rainbow(filename)
        elif event == 'Blackbody':
            blackbody(filename)
        elif event == "Iron":
            reds(filename)

    window.close()


if __name__ == '__main__':
    if os.path.exists('copied'):
        shutil.rmtree('copied')
        os.mkdir('copied')
    else:
        os.mkdir('copied')

    menus()
