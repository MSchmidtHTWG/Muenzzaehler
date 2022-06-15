from skimage import io
import numpy as np
import matplotlib.image as mimg
import cv2
from skimage.color import rgb2gray

def predict(regions):
    pass

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
    # binaryImage = highContrastToBinary(image)
    labeledImage = discreteContrast(sequentialLabeling(binaryImage))
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    regions = list()
    
    # for every region (label), compute its size and color
    labels, counts = np.unique(labeledImage, return_counts=True)
    # print(len(labels))
    # print(len(counts))
    for i in range(0,len(labels)-1):
        if counts[i] < minRegionSize:
            continue
        indizes = np.where(labeledImage == labels[i])
        colors = []
        for j in range(0, len(indizes[0])):
            colors.append(hsvImage[indizes[0][j]][indizes[1][j]])
        color = np.mean(colors)
        regions.append((counts[i], color))
        
    if return_steps:
        return regions, binaryImage, labeledImage, hsvImage
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

def removeClutter(array, threshold=1000):
    ret = []
    for i in array:
        if i > threshold:
            ret.append(i)
    return ret

def discreteContrast(filteredImage):
    shape = np.shape(filteredImage)
    img = filteredImage.copy()
    valueList = np.unique(img)
    valueDict = dict()
    for i in range(0, len(valueList)):
        valueDict.update({valueList[i] : i})
    for v in range(shape[0]):
        for u in range(shape[1]):
            img[v][u] = valueDict.get(filteredImage[v][u])
    return img

def labeledNeighbors(image, x, y, n=8):
    nbrs = list()
    if x - 1 >= 0 and image[y][x-1] > 1:
        nbrs.append((x-1, y))
    if n == 4:
        if y - 1 >= 0 and image[y-1][x] > 1:
            nbrs.append((x, y-1))
        return nbrs
    r = -1
    v = 2
    if x - 1 < 0:
        r = 0
    if x + 1 >= np.shape(image)[1]:
        v = 1
    if y - 1 >= 0:
        for i in range(r, v):
            if image[y-1][x+i] > 1:
                nbrs.append((x+i, y-1))
    return nbrs


def highContrastToBinary(image):
    img = rgb2gray(image)
    shape = np.shape(img)
    b_img = np.zeros((shape[0], shape[1]))
    for v in range(0, shape[0]):
        for u in range(0, shape[1]):
            if img[v][u] != 0:
                b_img[v][u] = 1
    return b_img


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