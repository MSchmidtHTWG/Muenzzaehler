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

''' Captures a high and a low contrast pic and processes those
@:return list of tuples for each region consisting of regionsize and mean tone
'''
def capture():
    cap = cv2.VideoCapture(0)
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
    layout = [
        [sg.Image(key="-TEST-", size=(160,120))],
        [sg.Text("Coins counted: 0€", key='-Count-')],
        [sg.Button("Process"), sg.Button("Coin count")],
        [sg.Image(key="-IMAGE-",size=(160,120)), sg.Image(key="-Binary-",size=(160,120))],
        [sg.Image(key="-Label-",size=(160,120)), sg.Image(key="-GroupImage-",size=(160,120))]
    ]

    # Create the window
    window = sg.Window("Coin Counter", layout, element_justification='c') # Alternative: layout ver grössern
    image = None
    regions = None
    test = np.zeros((120,160), dtype='uint8')
    io.imsave(f'../tmp/test.png', test)
    # Create an event loop
    while True:
        event, values = window.read(timeout=100)
        # End program if user closes window or
        # presses the OK button
        if event == "Process":
            filename = f'../testimages/test12.png'
            image = io.imread(filename)
            width = 160
            height = 120 # keep original height
            dim = (width, height)
            # resize image
            thumbnail = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/image.png', thumbnail)
            window['-IMAGE-'].update(filename=f'../tmp/image.png')
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
        if event == "Coin count":
            predict, groupImage = ci.predict(regions, np.shape(image))
            countedCoins = ci.count(predict)
            groupImage = np.array(groupImage, dtype='uint8')
            groupImage = cv2.resize(groupImage, dim, interpolation = cv2.INTER_AREA)
            io.imsave(f'../tmp/groupimage.png',groupImage)
            window['-Count-'].update("Coins counted: " + countedCoins)
            window['-GroupImage-'].update(filename=f'../tmp/groupimage.png')
        elif event == sg.WIN_CLOSED:
            break
        else:
            window['-TEST-'].update(filename=f'../tmp/test.png')
            window.refresh()
            test[30:90,40:120] += 1
            io.imsave(f'../tmp/test.png', test)
    window.close()

