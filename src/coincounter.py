import cv2
# from config import config
from skimage import io
import numpy as np
import os
import time
import sys
import coinimg as ci
import PySimpleGUI as sg
import os
from PIL import Image

import warnings

from houghtransform import HoughTransformCounter
warnings.filterwarnings("ignore")

def existing_images():
    extensions = ['.png']
    imagesList = []
    for r,d,files in (os.walk("../")):
        for file in files:
            if file.endswith(extensions[0]):
                imagesList.append(io.imread(os.path.join(r,file)))


    for image in imagesList:
        print(f"Es wurden {process(image)} Cent gezählt")

if __name__ == '__main__':
    dim = (160, 120)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    # GUI layout
    layout = [
        [sg.Image(key="-CAM-", size=(160,120))],
        [sg.Text("Region filter prediction: --", key='-Count-'), sg.Text("Houghtransform prediction: --", key='-HCount-')],
        [sg.Button("Capture"),sg.Button("Process"), sg.Button("Test"),sg.Button("Houghtransformation")],
        [sg.Image(key="-IMAGE-",size=(160,120))],
        [sg.Image(key="-Binary-",size=(160,120)), sg.Image(key="-GRAY-", size=dim)],
        [sg.Image(key="-Label-",size=(160,120)), sg.Image(key="-BLUR-", size=dim)],
        [sg.Image(key="-GroupImage-",size=(160,120)), sg.Image(key="-CIRCLES-", size=dim)],
    ]
    
    # Thumbnail dimensions
    

    # Create the window
    window = sg.Window("Coin Counter", layout, element_justification='c') # Alternative: layout ver grössern
    image = None
    regions = None
    cap = cv2.VideoCapture(0)
    filename = None

    # Create an event loop
    while True:
        event, values = window.read(timeout=10)
        if event == "Capture":
            window['-IMAGE-'].update(filename='',size=dim)
            window['-Binary-'].update(filename='',size=dim)
            window['-Label-'].update(filename='',size=dim)
            window['-GroupImage-'].update(filename='',size=dim)
            window['-GRAY-'].update(filename='',size=dim)
            window['-BLUR-'].update(filename='',size=dim)
            window['-CIRCLES-'].update(filename='',size=dim)
            window['-Count-'].update("Region filter prediction: --")
            window['-HCount-'].update("Houghtransform prediction: --")
            window.refresh()
            ret, frame = cap.read()
            cv2.imwrite(f'../tmp/image.png', frame)
            image = io.imread(f'../tmp/image.png')
            thumbnail = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            cv2.imwrite(f'../tmp/thumbnail.png', thumbnail)
            window['-IMAGE-'].update(filename=f'../tmp/thumbnail.png')
            window.refresh()  # End program if user closes window
            filename = '../tmp/image.png'
        elif event == "Test":
            window['-IMAGE-'].update(filename='',size=dim)
            window['-Binary-'].update(filename='',size=dim)
            window['-Label-'].update(filename='',size=dim)
            window['-GroupImage-'].update(filename='',size=dim)
            window['-GRAY-'].update(filename='',size=dim)
            window['-BLUR-'].update(filename='',size=dim)
            window['-CIRCLES-'].update(filename='',size=dim)
            window['-Count-'].update("Region filter prediction: --")
            window['-HCount-'].update("Houghtransform prediction: --")
            window.refresh()
            filename = f'../testimages/test12.png'
            image = io.imread(filename)
            thumbnail = cv2.resize(image,dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/thumbnail.png', thumbnail)
            window['-IMAGE-'].update(filename=f'../tmp/thumbnail.png')
            window.refresh()
            filename = '../testimages/test12.png'
        elif event == "Process":
            regions, binaryimage, labelImage = ci.regions(image, minRegionSize= 500, threshold=25, return_steps=True)
            binaryimage = cv2.resize(binaryimage, dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/binaryimage.png', binaryimage)
            window['-Binary-'].update(filename=f'../tmp/binaryimage.png')
            window.refresh()
            labelImage = cv2.resize(labelImage, dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/labelimage.png',labelImage)
            window['-Label-'].update(filename=f'../tmp/labelimage.png')
            window.refresh()
            predict, groupImage = ci.predict(regions, np.shape(image))
            countedCoins = ci.count(predict)
            groupImage = np.array(groupImage, dtype='uint8')
            groupImage = cv2.resize(groupImage, dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/groupimage.png',groupImage)
            window['-Count-'].update("Region filter prediction: " + countedCoins)
            window['-GroupImage-'].update(filename=f'../tmp/groupimage.png')
            window.refresh()        
        elif event == "Houghtransformation":
            a,b,c = HoughTransformCounter.run(path=filename)
            io.imsave(f'../tmp/gray.png', cv2.resize(b[0], dim, interpolation = cv2.INTER_AREA))
            io.imsave(f'../tmp/blur.png', cv2.resize(b[1], dim, interpolation = cv2.INTER_AREA))
            io.imsave(f'../tmp/circles.png', cv2.resize(b[2], dim, interpolation = cv2.INTER_AREA))
            window['-GRAY-'].update(filename=f'../tmp/gray.png')
            window['-BLUR-'].update(filename=f'../tmp/blur.png')
            window['-CIRCLES-'].update(filename=f'../tmp/circles.png')
            window['-HCount-'].update("Houghtransform prediction: " + a)
        elif event == sg.WIN_CLOSED:
            break
        else:
            if cap.isOpened():
                ret, frame = cap.read()
                cv2.imwrite(f'../tmp/cam.png', frame)
                window['-CAM-'].update(filename=f'../tmp/cam.png')
                window.refresh()
    window.close()

