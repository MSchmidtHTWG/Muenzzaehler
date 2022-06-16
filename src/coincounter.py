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
warnings.filterwarnings("ignore")

''' Captures a high and a low contrast pic and processes those
@:return list of tuples for each region consisting of regionsize and mean tone
'''
def capture():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ret, frame = cap.read()
    return frame

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
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    # GUI layout
    layout = [
        [sg.Image(key="-CAM-", size=(160,120))],
        [sg.Text("Coins counted: --", key='-Count-')],
        [sg.Button("Process"), sg.Button("Coin count"), sg.Button("Test")],
        [sg.Image(key="-IMAGE-",size=(160,120)), sg.Image(key="-Binary-",size=(160,120))],
        [sg.Image(key="-Label-",size=(160,120)), sg.Image(key="-GroupImage-",size=(160,120))]
    ]
    
    # Thumbnail dimensions
    dim = (160, 120)

    # Create the window
    window = sg.Window("Coin Counter", layout, element_justification='c') # Alternative: layout ver grössern
    image = None
    regions = None
    cap = cv2.VideoCapture(0)
    # Create an event loop
    while True:
        event, values = window.read(timeout=10)
        # End program if user closes window
        if event == "Process":
            window['-IMAGE-'].update(filename=None)
            window['-Binary-'].update(filename=None)
            window['-Label-'].update(filename=None)
            window['-GroupImage-'].update(filename=None)
            window['-Count-'].update("Coins counted: --")
            window.refresh()
            ret, frame = cap.read()
            cv2.imwrite(f'../tmp/image.png', frame)
            thumbnail = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            cv2.imwrite(f'../tmp/thumbnail.png', thumbnail)
            window['-IMAGE-'].update(filename=f'../tmp/thumbnail.png')
            window.Refresh()
            image = io.imread(f'../tmp/image.png')
            regions, binaryimage, labelImage = ci.regions(image, minRegionSize= 500, threshold=25, return_steps=True)
            binaryimage = cv2.resize(binaryimage, dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/binaryimage.png', binaryimage)
            window['-Binary-'].update(filename=f'../tmp/binaryimage.png')
            window.Refresh()
            labelImage = cv2.resize(labelImage, dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/labelimage.png',labelImage)
            window['-Label-'].update(filename=f'../tmp/labelimage.png')
            window.Refresh()             
        elif event == "Coin count":
            predict, groupImage = ci.predict(regions, np.shape(image))
            countedCoins = ci.count(predict)
            groupImage = np.array(groupImage, dtype='uint8')
            groupImage = cv2.resize(groupImage, dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/groupimage.png',groupImage)
            window['-Count-'].update("Coins counted: " + countedCoins)
            window['-GroupImage-'].update(filename=f'../tmp/groupimage.png')
        elif event == "Test":
            window['-IMAGE-'].update(filename=None)
            window['-Binary-'].update(filename=None)
            window['-Label-'].update(filename=None)
            window['-GroupImage-'].update(filename=None)
            window['-Count-'].update("Coins counted: --")
            window.refresh()
            filename = f'../testimages/test12.png'
            image = io.imread(filename)
            thumbnail = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/thumbnail.png', thumbnail)
            window['-IMAGE-'].update(filename=f'../tmp/thumbnail.png')
            window.Refresh()
            regions, binaryimage, labelImage = ci.regions(image, minRegionSize= 500, threshold=25, return_steps=True)
            binaryimage = cv2.resize(binaryimage, dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/binaryimage.png', binaryimage)
            window['-Binary-'].update(filename=f'../tmp/binaryimage.png')
            window.Refresh()
            labelImage = cv2.resize(labelImage, dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/labelimage.png',labelImage)
            window['-Label-'].update(filename=f'../tmp/labelimage.png')
            window.Refresh()      
        elif event == sg.WIN_CLOSED:
            break
        else:
            if cap.isOpened():
                ret, frame = cap.read()
                cv2.imwrite(f'../tmp/cam.png', frame)
                window['-CAM-'].update(filename=f'../tmp/cam.png')
                window.refresh()
    window.close()

