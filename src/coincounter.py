import cv2.cv2
from lib import Coinimage
from config import config
from skimage import io
import numpy as np
import os
import time
import sys




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
    existing_images()
    listeRegion = capture()
    coinsPredicted = predict(listeRegion)
    endResult = count(coinsPredicted)

