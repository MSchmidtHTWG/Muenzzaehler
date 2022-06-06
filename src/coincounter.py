import cv2.cv2
from lib import Coinimage
from config import config
from skimage import io
import numpy as np
import os
import time
import sys


def predict(regionlist):
    coins = config['coins']
    predictedCoins = []
    for region in regionlist:
        predictedCoin = None
        candidates = []
        for coin in coins:
            if coins.get(coin)[0] <= region[0] <= coins.get(coin)[1]:
                candidates.append(coin)
        if len(candidates) > 1:
            maxSize = sys.maxsize()
            for candidate in candidates:
                diff = abs(coins.get(coin)[2] - region[1])
                if (diff < maxSize):
                    maxSize= diff
                    predictedCoin = candidate          
        elif len(candidates) == 1:
            predictedCoin = candidates[0]
        predictedCoins.append(predictedCoin)
    return predictedCoins

''' Captures a high and a low contrast pic and processes those
@:return list of tuples for each region consisting of regionsize and mean tone
'''
def capture():
    # nehme high und low contrast auf
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
    # regionen filter auf high
    return process(lowcontrast,highcontrast)


''' 
@:return list of tuples for each region consisting of regionsize and mean tone
'''
def process(lowcontrast, highcontrast):
    hsvImg = cv2.cvtColor(lowcontrast, cv2.COLOR_BGR2HSV)
    regions = Coinimage(highcontrast).highContrastToBinary().sequentialLabeling()
    # für jede region farbe aus low ziehen und area size der region
    labels, counts = np.unique(regions.image, return_counts=True)
    counts = counts[0:len(counts)-1]
    shape = np.shape(regions.image)
    colors = []
    
    for label in labels[0, len(label)-1]:
        color = []
        for v in range(0, shape[0]):
            for u in range(0, shape[1]):
                if regions.image[v][u] == label:
                    color.append(hsvImg[v][u][0])
        colors.append(np.mean(color))
    regionlist = []
    for i in range(0, len(colors)):
        regionlist.append((counts[i], colors[i]))
    
    return regionlist
    

''' Tries to create a prediction off all Pictures found recursiveliy from root
'''
def existing_images():
    extensions = ['.png']
    imagesList = []
    for r,d,files in (os.walk("../")):
        for file in files:
            if file.endswith(extensions[0]):
                imagesList.append(io.imread(os.path.join(r,file)))

    # TODO 2 BIlder übergeben
    for image in imagesList:
        print(f"Es wurden {process(image)} Cent gezählt")


'''Counts the Value of the Coins
'''
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
    for i in range(0,5):
        lowcontrast = io.imread(f'../reference/test{i}.png')
        highcontrast = io.imread(f'../reference/test{i}.png')
        listeRegion = process(lowcontrast, highcontrast)
        coinsPredicted = predict(listeRegion)
        endResult = count(coinsPredicted)
        print(f'test{i}.png: ' + str(endResult))
    
