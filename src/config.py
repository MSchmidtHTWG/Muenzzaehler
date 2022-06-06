from typing import Dict, Any
import sys
import numpy as np
from skimage import io
import cv2

from lib import Coinimage

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
            path = io.imread(f'./reference/highContrast/{n}{i}.png')
            labeledImage = Coinimage(path).highContrastToBinary().sequentialLabeling().image
            valueList, counts = np.unique(labeledImage, return_counts=True)
            count = np.max(counts[0:len(counts)-1])
            colorImage = io.imread(f'./reference/lowContrast/{n}{i}.png')
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
    return  sizeAndToneDict

coins = regionSizeAndTone()
config: dict[Any, Any] = {

    "camera-settings": {
        "highcontrast": {
            "width": 640,
            "brightness": 180,
            "contrast": 255,
            "saturation": 0,
            "gain": 32,
            "exposure": -2,
            "white balance": 1,
        },
        "lowcontrast": {
            "width": 640,
            "brightness": 0,
            "contrast": 0,
            "saturation": 0,
            "gain": 0,
            "exposure": 0,
            "white balance": 1,
        },
    },
    "coins": coins
}
print(coins)
print(config['coins'])
