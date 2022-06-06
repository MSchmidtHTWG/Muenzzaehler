from skimage import io
import numpy as np
import matplotlib.image as mimg
import cv2
from skimage.color import rgb2gray

def removeClutter(array, threshold=1000):
    ret = []
    for i in array:
        if i > threshold:
            ret.append(i)
    return ret

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


def sequentialLabeling(image, n=8):
    # img = invertedBinaryImage(image)
    img = image.copy()
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