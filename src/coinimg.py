from skimage import io
import numpy as np
import matplotlib.image as mimg
import cv2
from skimage.color import rgb2gray
from math import pi
import pickle
import os
import sys


def predict_hough(coins: [(int, float)]) -> str:
    '''
    @:param coins as list of tuples that represent a coin (pixelamount as int, mean_hue value)
    @:return a String with the amount
    '''
    # coins = loadDict(hough=True)
    return count(predict(coins))


def predict(regions, shape=None):
    coins = loadDict()
    if not shape is None:
        groupImage = np.full(shape, 255)
    predictions = []
    for region in regions:
        diffColor = sys.maxsize
        group1 = {'2Euro', '1Euro'}
        group2 = {'50Cent', '20Cent', '10Cent'}
        group3 = {'5Cent', '2Cent', '1Cent'}
        for candidate in coins:
            diffRegionColor = abs(coins.get(candidate)[2] - region[1])
            if diffRegionColor < diffColor:
                diffColor = diffRegionColor
                closest_color_candidate = candidate
        if group1.issuperset({closest_color_candidate}):
            colorCandidates = group1
        elif group2.issuperset({closest_color_candidate}):
            colorCandidates = group2
        else:
            colorCandidates = group3
        # print(colorCandidates)
        candidates = set()
        diffSize = sys.maxsize
        for candidate in colorCandidates:
            if coins.get(candidate)[0] <= region[0] <= coins.get(candidate)[1]:
                candidates.add(candidate)
            diffMinSize = abs(coins.get(candidate)[0] - region[0])
            diffMaxSize = abs(coins.get(candidate)[1] - region[0])
            if diffMinSize < diffSize:
                diffSize = diffMinSize
                closest_size_candidate = candidate
            if diffMaxSize < diffSize:
                diffSize = diffMaxSize
                closest_size_candidate = candidate
        if len(candidates) == 1:
            # print('size match')
            # print(candidates)
            predictions.append(candidates.pop())
        else:
            # print('no size match')
            # print(closest_size_candidate)
            predictions.append(closest_size_candidate)
        if not shape is None:
            if predictions[len(predictions) - 1] == '2Euro':
                r = 102
                g = 204
                b = 255
            elif predictions[len(predictions) - 1] == '1Euro':
                r = 0
                g = 153
                b = 230
            elif predictions[len(predictions) - 1] == '50Cent':
                r = 255
                g = 230
                b = 128
            elif predictions[len(predictions) - 1] == '20Cent':
                r = 255
                g = 209
                b = 26
            elif predictions[len(predictions) - 1] == '10Cent':
                r = 204
                g = 163
                b = 0
            elif predictions[len(predictions) - 1] == '5Cent':
                r = 255
                g = 133
                b = 102
            elif predictions[len(predictions) - 1] == '2Cent':
                r = 255
                g = 71
                b = 26
            elif predictions[len(predictions) - 1] == '1Cent':
                r = 204
                g = 41
                b = 0
            for i in range(0, len(region[2][0])):
                groupImage[region[2][0][i]][region[2][1][i]][0] = r
                groupImage[region[2][0][i]][region[2][1][i]][1] = g
                groupImage[region[2][0][i]][region[2][1][i]][2] = b
        # print('=======================================')
    if not shape is None:
        return predictions, groupImage
    return predictions


def count(predictions):
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
    for prediction in predictions:
        result += coin.get(prediction)
    return str(result / 100) + '€'


def coindict():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    names = ['2Euro', '1Euro', '50Cent', '20Cent', '10Cent', '5Cent', '2Cent', '1Cent']
    size = 5
    cd = dict()
    for name in names:
        region_colors = []
        max_region_size = 0
        min_region_size = sys.maxsize
        for i in range(0, size):
            image = io.imread(f'../reference/{name}{i}.png')
            region = regions(image, minRegionSize=1500, threshold=25)
            m = 0
            x = None
            for r in region:
                if r[0] > m:
                    m = r[0]
                    x = r
            region.clear()
            region.append(x)
            print(name + str(i) + ':' + str(len(region)))
            assert len(region) == 1
            if region[0][0] > max_region_size:
                max_region_size = region[0][0]
            if region[0][0] < min_region_size:
                min_region_size = region[0][0]
            region_colors.append(region[0][1])
        color = np.mean(region_colors)
        cd.update({name: (min_region_size, max_region_size, color)})
    return cd


def loadDict(hough=False):
    if hough:
        with open('coin_dictionary_hough.pkl', 'rb') as f:
            cd = pickle.load(f)
        return cd
    with open('coin_dictionary.pkl', 'rb') as f:
        cd = pickle.load(f)
    return cd


def saveDict(hough=False):
    if hough:
        with open('coin_dictionary_hough.pkl', 'wb') as f:
            pickle.dump(dictionary, f)
    dictionary = coindict()
    with open('coin_dictionary.pkl', 'wb') as f:
        pickle.dump(dictionary, f)


'''
Computes region sizes and region colors from a 24bit rgb image. 
The image will be binarized with @threshold differentiating between
foreground and background, then it will be labeled.
For color extraction, the image will be converted from RGB to HSV.
Regions smaller than @minSize are discarded. The highest label (background)
is discarded as well.
@return: returns a list of tuples for each region. Each tuple contains a regions size and its color.
         If return_steps=True, returns the list of tuples and three intermediary images from the processing steps.
'''


def regions(image, minRegionSize=0, threshold=0, return_steps=False):
    binaryImage = rgbToBinary(image, threshold)
    labeledImage = sequentialLabeling(binaryImage)
    hsvImage = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    regions = list()

    # for every region (label), compute its size and color
    labels, counts = np.unique(labeledImage, return_counts=True)
    for i in range(0, len(labels) - 1):
        if counts[i] < minRegionSize:
            labeledImage[labeledImage == labels[i]] = labels[len(labels) - 1]
            continue
        indizes = np.where(labeledImage == labels[i])
        colors = []
        for j in range(0, len(indizes[0])):
            colors.append(hsvImage[indizes[0][j]][indizes[1][j]][0])
        color = np.mean(colors)
        regions.append((counts[i], color, indizes))

    if return_steps:
        return regions, binaryImage, discreteContrast(labeledImage)
    return regions


def rgbToBinary(coloredImage, threshold):
    img = rgb2gray(coloredImage)
    shape = np.shape(img)
    normalized_image = img / np.amax(img)
    normalized_threshold = threshold / 255
    b_img = np.zeros((shape[0], shape[1]))
    for v in range(0, shape[0]):
        for u in range(0, shape[1]):
            if normalized_image[v][u] > normalized_threshold:
                b_img[v][u] = 1
    return b_img


def discreteContrast(filteredImage):
    shape = np.shape(filteredImage)
    img = filteredImage.copy()
    valueList = np.unique(img)
    valueDict = dict()
    for i in range(0, len(valueList)):
        valueDict.update({valueList[i]: i})
    for v in range(shape[0]):
        for u in range(shape[1]):
            img[v][u] = valueDict.get(filteredImage[v][u])
    return img


def labeledNeighbors(image, x, y, n=8):
    nbrs = list()
    if x - 1 >= 0 and image[y][x - 1] > 1:
        nbrs.append((x - 1, y))
    if n == 4:
        if y - 1 >= 0 and image[y - 1][x] > 1:
            nbrs.append((x, y - 1))
        return nbrs
    r = -1
    v = 2
    if x - 1 < 0:
        r = 0
    if x + 1 >= np.shape(image)[1]:
        v = 1
    if y - 1 >= 0:
        for i in range(r, v):
            if image[y - 1][x + i] > 1:
                nbrs.append((x + i, y - 1))
    return nbrs


def sequentialLabeling(binaryImage, n=8):
    img = binaryImage.copy()
    m = 2
    c = list()
    for v in range(0, np.shape(img)[0]):
        for u in range(0, np.shape(img)[1]):
            if img[v][u] == 1:
                nbrs = labeledNeighbors(img, u, v, n)
                if len(nbrs) == 0:
                    img[v][u] = m
                    m = m + 1
                elif len(nbrs) == 1:
                    p = nbrs[0]
                    img[v][u] = img[p[1]][p[0]]
                elif len(nbrs) > 1:
                    p = nbrs.pop(0)
                    k = img[p[1]][p[0]]
                    img[v][u] = k
                    for p in nbrs:
                        ni = img[p[1]][p[0]]
                        if ni != k:
                            c.append({ni, k})
    r = list()
    for i in range(2, m):
        r.append({i})
    for collisions in c:
        a = collisions.pop()
        b = collisions.pop()
        for labelsets in r:
            if labelsets.issuperset({a}):
                ra = labelsets
            if labelsets.issuperset({b}):
                rb = labelsets
        if ra.isdisjoint(rb):
            ra.update(rb)
            r.remove(rb)
    for v in range(0, np.shape(img)[0]):
        for u in range(0, np.shape(img)[1]):
            if img[v][u] > 1:
                for lsets in r:
                    if lsets.issuperset({img[v][u]}):
                        img[v][u] = min(lsets)
    return invert(img)


def invert(image):
    img = image.copy()
    img = (img * -1) + np.amax(image)
    return img
