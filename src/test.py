import cv2
from config import config
from skimage import io
import numpy as np
import os
import time
import sys
import coinimg as ci

img = io.imread('C://Muenzzaehler/reference/highContrast/2Euro0.png')
cimg = cv2.cvtColor(io.imread('C://Muenzzaehler/reference/lowContrast/2Euro0.png'), cv2.COLOR_BGR2HSV)
sql = ci.sequentialLabeling(ci.highContrastToBinary(img))
shape = np.shape(sql)
labels, counts = np.unique(sql, return_counts=True)
labels = labels[0:len(labels)-1]
counts = counts[0:len(counts)-1]
colors = list()
for label in labels:
    for v in range(0, shape[0]):
        for u in range(0, shape[1]):
            if sql[v][u] - label == 0:
                colors.append(cimg[v][u][0])
print(labels)
print(counts)
# print(colors)
print(max(colors))
print(min(colors))
print(np.mean(colors))
print(len(colors))