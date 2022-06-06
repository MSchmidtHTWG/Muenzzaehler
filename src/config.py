from typing import Dict, Any
import sys
import numpy as np
from skimage import io
import cv2

# from lib import Coinimage
import coinimg as ci

def regionSizeAndTone():
    # names = ['2Euro', '1Euro', '50Cent', '20Cent', '10Cent', '5Cent', '2Cent', '1Cent']
    names = ['2Euro', '1Euro', '20Cent', '10Cent']
    # names = ['2Euro']
    size = 5
    sizeAndToneDict = dict()
    color = list()
    for n in names:
        mi  = sys.maxsize
        mx = 0
        color.clear()
        # print(len(color))
        for i in range(0, size):
            img = io.imread(f'C://Muenzzaehler/reference/highContrast/{n}{i}.png')
            colorImage = io.imread(f'C://Muenzzaehler/reference/lowContrast/{n}{i}.png')
            hsvImg = cv2.cvtColor(colorImage, cv2.COLOR_BGR2HSV)
            labeledImage = ci.sequentialLabeling(ci.highContrastToBinary(img))
            shape = np.shape(labeledImage)
            labels, counts = np.unique(labeledImage, return_counts=True)
            counts = counts[0:len(counts)-1]
            labels = labels[0:len(labels)-1]
            ccounts = []
            clabels = []
            for i in range(0, len(counts)):
                if counts[i] > 2000:
                    ccounts.append(counts[i])
                    clabels.append(labels[i])
            counts = ccounts
            labels = clabels
            count = np.max(counts)
            for label in labels:
                for v in range(0, shape[0]):
                    for u in range(0, shape[1]):
                        if labeledImage[v][u] == label:
                            color.append(hsvImg[v][u][0])
            if count <= mi:
                mi = count
            if count >= mx:
                mx = count
        # colors = list()
        # for c in color:
        #     colors.append(int(c))
        # print(sum(color))
        # print(str(sum(color[0:4]) / 5))
        # print(np.shape(color))
        # print(max(color))
        # print(np.median(color[0]))
        # print(int(color[0]))
        # print(np.median(colors))
        # print(len(color))
        # print(max(color))
        # print(min(color))
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
