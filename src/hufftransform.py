import numpy as np
import cv2 as cv


class HufftransformCounter:

    @staticmethod
    def run(**kwargs) -> (int, float):
        """
        :param kwargs: image as image=np.array of the image or path as  'path=/path/to/image'
        :return a Tuple with (amount in cents, probability)
        """

        def getCircles(image: np.array) -> {}:
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            src = image.copy()
            blured = cv.medianBlur(gray, 5)
            rows = gray.shape[0]
            return cv.HoughCircles(blured, cv.HOUGH_GRADIENT, 1, rows / 8, param1=100, param2=30, minRadius=10)

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

        def getColor(circles, image):
            def swapAxis(circles) -> np.array:
                swapedAxes = []
                for element in circles:
                    element = element[0]
                    swapedAxes.append((element[1], element[0], element[2]))
                return np.array(swapedAxes)

            return None

        def swapAxis(circles) -> np.array:
            swapedAxes = []
            for element in circles:
                element = element[0]
                swapedAxes.append((element[1], element[0], element[2]))
            return np.array(swapedAxes)

        def getMinSquare(circle) -> (int, int, int, int):
            return circle[0] - circle[2], circle[0] + circle[2], circle[1] - circle[2], circle[1] + circle[2]

        def getCoinCoord(circle) -> []:
            result = []
            circleX = circle[0]
            circleY = circle[1]
            radius = circle[2]
            xMin, xMax, yMin, yMax = getMinSquare(circle)
            for x in range(xMin, xMax):
                # inner=[]
                for y in range(yMin, yMax):
                    dx = x - circleX
                    dy = y - circleY
                    squareDistance = dx ** 2 + dy ** 2
                    if squareDistance <= radius ** 2:
                        result.append((x, y))
            return np.array(result)

        def getColor(image, coords: []):
            hsvImage = cv.cvtColor(image, cv.COLOR_RGB2HSV)
            colors = []
            for element in coords:
                color = hsvImage[element[0], element[1]]
                colors.append(color[0])
                print(color)
            return np.median(colors)

        if "image" in kwargs.keys():
            image = kwargs['image']
        elif "path" in kwargs.keys():
            image = cv.imread(kwargs['path'], cv.IMREAD_COLOR)
        else:
            raise ValueError(
                "You either need to pass the image as 'image=np.array' or the path to the image as 'path=/path/to/image'")

        circles = getCircles(image)
        colors = []
        for circle in circles:
            coords = getCoinCoord(circle)
            color = getColor(image, coords=coords)

        image = image.copy()
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        bluredImage = cv.medianBlur(gray, 5)
        rows = gray.shape[0]
        # cv.imwrite('tmp.png',drawCircles(circles, image)) # anzeigen der erkannten Münzen


        return circles


if __name__ == '__main__':
    HufftransformCounter.run(path='../testimages/0.png')
