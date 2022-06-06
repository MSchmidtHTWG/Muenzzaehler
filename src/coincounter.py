import cv2.cv2
from lib import Coinimage
# from config import config
from skimage import io
import numpy as np
import os
import time
import sys

coins = None

def regionSizeAndTone():
    # names = ['2Euro', '1Euro', '50Cent', '20Cent', '10Cent', '5Cent', '2Cent', '1Cent']
    # names = ['2Euro', '1Euro', '20Cent', '10Cent']
    names = ['2Euro']
    size = 1
    sizeAndToneDict = dict()
    for n in names:
        mi  = sys.maxsize
        mx = 0
        color = []
        for i in range(0, size):
            path = io.imread(f'C:/Muenzzaehler/reference/highContrast/{n}{i}.png')
            labeledImage = Coinimage(path)
            labeledImage = labeledImage.highContrastToBinary()
            labeledImage = labeledImage.sequentialLabeling()
            labeledImage = labeledImage.image
            valueList, counts = np.unique(labeledImage, return_counts=True)
            count = np.max(counts[0:len(counts)-1])
            colorImage = io.imread(f'C:/Muenzzaehler/reference/lowContrast/{n}{i}.png')
            hsvImg = cv2.cvtColor(colorImage, cv2.COLOR_BGR2HSV)
            shape = np.shape(labeledImage)
            for label in valueList:
                for v in range(0, shape[0]):
                    for u in range(0, shape[1]):
                        if labeledImage[v][u] == label:
                            color.append(hsvImg[v][u][0])
            if count <= mi:
                mi = count
            if count >= mx:
                mx = count
        sizeAndToneDict.update({n : (mi, mx, np.mean(color))})
    return sizeAndToneDict

def predict(regionlist):
    # coins = config['coins']
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

def predict(image):
    return 10

'''
@:param image where to count the money
'''
def process(image):  # rückgabe Geldwert in cent zBsp.
    img = Coinimage(image)
    img = img.invert()
    img = img.discreteContrast()
    img  = img.highContrastToBinary()
    img = img.sequentialLabeling()
    img = img.countAreaSize()
    return predict(img)


''' Tries to create a prediction off all Pictures found recursiveliy from root
'''
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
    for i in range(0,5):
        lowcontrast = io.imread(f'../reference/test{i}.png')
        highcontrast = io.imread(f'../reference/test{i}.png')
        listeRegion = process(lowcontrast, highcontrast)
        coinsPredicted = predict(listeRegion)
        endResult = count(coinsPredicted)
        print(f'test{i}.png: ' + str(endResult))
    print(1)
    coins = regionSizeAndTone()
    print(coins)
    # for i in range(0,5):
    #     lowcontrast = io.imread(f'../reference/test{i}.png')
    #     highcontrast = io.imread(f'../reference/test{i}.png')
    #     listeRegion = process(lowcontrast, highcontrast)
    #     coinsPredicted = predict(listeRegion)
    #     endResult = count(coinsPredicted)
    #     print(f'test{i}.png: ' + str(endResult))

