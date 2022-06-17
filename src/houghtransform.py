from math import ceil, floor, nan
from coinimg import predict_hough
from skimage import io
import numpy as np
import cv2 as cv


class HoughTransformCounter:

    @staticmethod
    def run(**kwargs) -> (int, list, float):
        """
        :param kwargs: image as image=np.array of the image or path as  'path=/path/to/image'
        :return a Tuple with (amount as String, list of 3 Images, probability)
        """

        def getCircles(image: np.array) -> ({}, np.array, np.array):
            image = image.copy()
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            blured = cv.medianBlur(gray, 5)
            rows = gray.shape[0]
            return cv.HoughCircles(blured, cv.HOUGH_GRADIENT, 1, rows / 8, param1=100, param2=30,
                                   minRadius=10), gray, blured

        def drawCircles(circles, image):
            image = image.copy()
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    print(f"x={i[0]}, y={i[1]}, radius={i[2]}")
                    center = (i[0], i[1])
                    # circle center
                    cv.circle(image, center, 1, (0, 100, 100), 3)
                    # circle outline
                    radius = i[2]
                    cv.circle(image, center, radius, (255, 0, 255), 3)
                return image

        def getMinSquare(circle) -> (int, int, int, int):
            return circle[0] - circle[2], circle[0] + circle[2], circle[1] - circle[2], circle[1] + circle[2]

        def getCoinCoord(circle, xMaxImage, yMaxImage) -> []:
            result = []
            circleX = circle[0]
            circleY = circle[1]
            radius = circle[2]
            xMin, xMax, yMin, yMax = getMinSquare(circle)
            xMax = min(xMaxImage, xMax)
            yMax = min(yMaxImage, yMax)
            tmpxMax = 0
            tmpyMax = 0
            for x in range(ceil(xMin), floor(xMax)):
                for y in range(ceil(yMin), floor(yMax)):
                    dx = x - circleX
                    dy = y - circleY
                    squareDistance = dx ** 2 + dy ** 2
                    if squareDistance <= radius ** 2:
                        result.append((x, y))
            return np.array(result)

        def getColor(image, coords: []):
            """Die Methode erhält ein RGB Bild und berechnet den Median HSV hue wert über alle koordinaten
            @param image as RGB  Image/np.array
            @:param coords Liste aus Koordinaten Tupel [(x,y)]
            """
            hsvImage = cv.cvtColor(image, cv.COLOR_RGB2HSV)
            colors = []
            rgb = [0, 0, 0]
            for element in coords:
                color = hsvImage[element[1], element[0]]  # ??? x und y koordinaten sind in np.array invertiert
                colors.append(color[0])
            return np.mean(colors)

        def predictAll(all: []) -> str:
            '''add the prediction -> match color and radius to a coin'''
            return predict_hough(all)

        if "image" in kwargs.keys():
            image = kwargs['image']
        elif "path" in kwargs.keys():
            image = io.imread(kwargs['path'])
        else:
            raise ValueError(
                "You either need to pass the image as 'image=np.array' or the path to the image as 'path=/path/to/image'")

        coins, gray, blured = getCircles(image)
        coinData = []
        for circle in coins[0]:
            coords = getCoinCoord(circle, xMaxImage=image.shape[1], yMaxImage=image.shape[0])
            color = getColor(image, coords=coords)
            coinData.append((len(coords), color))
        probability = nan  # currently not calculated
        # argument is list of tuples (regionSize, mean hsv color)
        return predictAll(coinData), [gray,blured, drawCircles(coins, image)],probability


if __name__ == '__main__':
    amount = HoughTransformCounter.run(path='../testimages/test12.png')
    print(amount)
