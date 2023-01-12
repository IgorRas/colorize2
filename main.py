import PySimpleGUI as sg
from PIL import Image
import shutil
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# wybranie obrazu do obróbki
def select(filename):
    img = cv2.imread(filename, 0)
    im = Image.fromarray(img)
    im.thumbnail(size=(900, 900))
    im.save(filename, format="PNG")
    layout = [[sg.Image(filename)]]
    return sg.Window(filename, layout, location=(800, 600), resizable=True, finalize=True)


def save_image(filename):
    img = Image.open(filename)
    path_to = sg.popup_get_folder('file to open', no_window=True)
    img.save(f'{path_to}/smoothed.png', format='PNG')
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
    fin_img = fin_img.astype(int)
    plt.imsave('copied/smooth.jpg', fin_img)


def mono1(filename):
    img = mpimg.imread(filename)
    plt.imshow(img, cmap='Greys')
    plt.show()


def mono2(filename):
    img = mpimg.imread(filename)
    plt.imshow(img, cmap='Greys_r')
    plt.show()


def spectrum(filename):
    img = mpimg.imread(filename)
    plt.imshow(img, cmap='hsv')
    plt.show()


def rainbow(filename):
    img = mpimg.imread(filename)
    plt.imshow(img, cmap='rainbow')
    plt.show()


def blackbody(filename):
    img = mpimg.imread(filename)
    plt.imshow(img, cmap='autumn')
    plt.show()


def reds(filename):
    img = mpimg.imread(filename)
    plt.imshow(img, cmap='Reds')
    plt.show()


def custom(filename, colors):
    img = mpimg.imread(filename)
    # colors = ["darkorange", "gold", "lawngreen", "lightseagreen"]
    cmap1 = LinearSegmentedColormap.from_list("mycmap", colors)
    plt.imshow(img, cmap=cmap1)
    plt.show()


def colors():
    layout = [[sg.Image('copied/fig.png')],
        [[sg.Image('obrazy/b.png', pad=10), sg.Image('obrazy/c.png', pad=10), sg.Image('obrazy/k.png', pad=10)],
        [sg.Image('obrazy/green.png', pad=10), sg.Image('obrazy/m.png', pad=10), sg.Image('obrazy/w.png', pad=10)],
        [sg.Image('obrazy/r.png', pad=10), sg.Image('obrazy/y.png', pad=10), sg.Image('obrazy/g.png', pad=10)]],
        [[sg.Checkbox('B', default=False), sg.Checkbox('C', default=False), sg.Checkbox('K', default=False)],
         [sg.Checkbox('G', default=False), sg.Checkbox('M', default=False), sg.Checkbox('W', default=False)],
         [sg.Checkbox('R', default=False), sg.Checkbox('Y', default=False), sg.Checkbox('G', default=False)]],
        [sg.Submit()]
    ]
    n_window = sg.Window('Podaj dane', layout, element_justification='center')
    event, values = n_window.read()
    n_window.close()
    cols = ['b', 'c', 'k', 'g', 'm', 'w', 'r', 'y', 'gray']
    truths = [values[10], values[11], values[12], values[13], values[14], values[15], values[16], values[17], values[18]]
    chosen = dict(zip(cols, truths))
    end = list(filter(lambda x: chosen[x] == True, chosen))
    return end


def histogram(filename):
    img = cv2.imread(filename, 0)
    # histogram of image
    plt.hist(img.ravel(), 256, [0, 256])
    plt.savefig('copied/fig.png', bbox_inches='tight')
    plt.close()


def menus():
    sg.theme('LightGreen')
    sg.set_options(element_padding=(0, 0))

    # opcje menu
    menu_def = [['&File', ['&Open', 'Save']],
                ['&Modify', ['Smoothing']],
                ['Colorize', ['Monochrome(1)', 'Monochrome(2)', 'Spectrum', 'Rainbow', 'Blackbody', 'Iron', 'Custom']]]

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
            filename = sg.popup_get_file('file to open', no_window=True)
            new_window = select(filename)
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
        elif event == 'Custom':
            histogram(filename)
            colory = colors()

            custom(filename, colory)

    window.close()


if __name__ == '__main__':
    if os.path.exists('copied'):
        shutil.rmtree('copied')
        os.mkdir('copied')
    else:
        os.mkdir('copied')

    menus()
