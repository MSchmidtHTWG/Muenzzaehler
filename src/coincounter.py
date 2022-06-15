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
    colorCandidates = set()
    sizeCandidates = set()
    


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
    cap.set(15, config['camera-settings']['highcontrast']['exposure'])
    cap.set(14, config['camera-settings']['highcontrast']['gain'])
    cap.set(10, config['camera-settings']['highcontrast']['brightness'])
    cap.set(11, config['camera-settings']['highcontrast']['contrast'])
    cap.set(12, config['camera-settings']['highcontrast']['tone'])
    cap.set(17, config['camera-settings']['highcontrast']['whitebalance'])
    time.sleep(0.5)
    ret, highcontrast = cap.read()
    cap = cv2.VideoCapture(0)
    cap.set(15, config['camera-settings']['lowcontrast']['exposure'])
    cap.set(14, config['camera-settings']['lowcontrast']['gain'])
    cap.set(10, config['camera-settings']['lowcontrast']['brightness'])
    cap.set(11, config['camera-settings']['lowcontrast']['contrast'])
    cap.set(12, config['camera-settings']['lowcontrast']['tone'])
    cap.set(17, config['camera-settings']['lowcontrast']['whitebalance'])
    time.sleep(0.5)
    ret, lowcontrast = cap.read()
    return process(lowcontrast,highcontrast)


def process(lowcontrast, highcontrast):
    hsvImg = cv2.cvtColor(lowcontrast, cv2.COLOR_BGR2HSV)
    regions = ci.sequentialLabeling(ci.highContrastToBinary(highcontrast))
    labels, counts = np.unique(regions, return_counts=True)
    print(len(labels))
    counts = counts[0:len(counts)-1]
    labels = labels[0:len(labels)-1]
    ccounts = []
    clabels = []
    shape = np.shape(regions)
    colors = []
    for i in range(0, len(counts)):
        if counts[i] > 1000:
            ccounts.append(counts[i])
            clabels.append(labels[i])
    counts = ccounts
    labels = clabels
    print(len(labels))
    for label in labels:
        color = []
        for v in range(0, shape[0]):
            for u in range(0, shape[1]):
                if regions[v][u] == label:
                    color.append(int(hsvImg[v][u][0]))
        colors.append(np.mean(color))
    regionlist = []
    for i in range(0, len(colors)):
        regionlist.append((counts[i], colors[i]))

    return regionlist

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

