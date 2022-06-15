import cv2
from config import config
from skimage import io
import numpy as np
import os
import time
import sys
import coinimg as ci
import PySimpleGUI as sg
import os

coins = config['coins']

def predict2(regions):
    predictions = []
    for region in regions:
        colorCandidates = set()
        sizeCandidates = set()
        closest_size_candidate = ''
        closest_color_candidate = ''
        diffSize = sys.maxsize
        diffColor = sys.maxsize

        for coin in coins:
            if coins.get(coin)[0] <= region[0] <= coins.get(coin)[1]:
                sizeCandidates.add(coin)
            diffMinSize = abs(coins.get(coin)[0] - region[0])
            diffMaxSize = abs(coins.get(coin)[1] - region[0])
            if diffMinSize < diffSize:
                diffSize = diffMinSize
                closest_size_candidate = coin
            if diffMaxSize < diffSize:
                diffSize = diffMaxSize
                closest_size_candidate = coin
            diffRegionColor = abs(coins.get(coin)[2] - region[1])
            if diffRegionColor < diffColor:
                diffColor = diffRegionColor
                closest_color_candidate = coin
        if len(sizeCandidates) == 1:
            predictions.add(sizeCandidates.pop)
        elif len(sizeCandidates) == 0:
            predictions.add(closest_size_candidate)
        else:
            predictions.add(closest_color_candidate)
    return predictions

def predict(regionlist):
    predictedCoins = []
    for region in regionlist:
        predictedCoin = None
        candidates = []
        for coin in coins:
            if coins.get(coin)[0] <= region[0] <= coins.get(coin)[1]:
                candidates.append(coin)
        if len(candidates) > 1:
            maxSize = sys.maxsize
            for candidate in candidates:
                diff = abs(coins.get(candidate)[2] - region[1])
                if diff < maxSize:
                    maxSize = diff
                    predictedCoin = candidate          
        elif len(candidates) == 1:
            predictedCoin = candidates[0]
        else:
            maxSize = sys.maxsize
            for coin in coins:
                diff = abs(coins.get(coin)[0] - region[0])
                diff2 = abs(coins.get(coin)[1] - region[0])
                if diff < maxSize:
                    maxSize = diff
                    predictedCoin = coin
                if diff2 < maxSize:
                    maxSize = diff2
                    predictedCoin = coin
        predictedCoins.append(predictedCoin)
    return predictedCoins

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


def with_cam():
    pass

# alle Cents zählen
def count(predictedCoins):
    result = 0
    coin = {
        '2Euro': 200,
        '1Euro': 100,
        '50Cent': 50,
        '20Cent': 20,
        '10Cent': 10,
        '5Cent': 5,
        '2Cent': 2,
        '1Cent': 1
    }
    for predictedCoin in predictedCoins:
        result += coin.get(predictedCoin)
    return result

if __name__ == '__main__':
    # for i in range(0,5):
    #     lowcontrast = io.imread(f'C://Muenzzaehler/reference/lowContrast/test{i}.png')
    #     highcontrast = io.imread(f'C://Muenzzaehler/reference/highContrast/test{i}.png')
    #     regions = process(lowcontrast, highcontrast)
    #     print(regions)
    #     coinPredictions = predict(regions)
    #     print(coinPredictions)
    #     result = count(coinPredictions)
    #     print(f'test{i}.png: ' + str(result))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")], [sg.Image(key="-IMAGE-")]]

    # Create the window
    window = sg.Window("Demo", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK":
            # filename = 'C://Muenzzaehler/reference/highContrast/2Euro0.png'
            filename = f'../reference/highContrast/2Euro0.png'
            window['-IMAGE-'].update(filename=filename)
        elif event == sg.WIN_CLOSED:
            break

    window.close()

