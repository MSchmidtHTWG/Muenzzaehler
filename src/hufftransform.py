import numpy as np
import cv2 as cv


class HufftransformCounter:

    @staticmethod
    def run(**kwargs) -> (int, float):
        """
        :param kwargs: image as image=np.array of the image or path as  'path=/path/to/image'
        :return a Tuple with (amount in cents, probability)
        """
        if "image" in kwargs.keys():
            image = kwargs['image']
        elif "path" in kwargs.keys():
            image = cv.imread(kwargs['path'], cv.IMREAD_COLOR)
        else:
            raise ValueError(
                "You either need to pass the image as 'image=np.array' or the path to the image as 'path=/path/to/image'")

        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        circles = HufftransformCounter.__getCircles(image)
        color = HufftransformCounter.__getColor(circles, image)
        print()

    def __getCircles(image: np.array) -> {}:
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

        image = image.copy()
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        bluredImage = cv.medianBlur(gray, 5)
        rows = gray.shape[0]
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8, param1=100, param2=30, minRadius=10)
        # cv.imwrite('tmp.png',drawCircles(circles, image)) # anzeigen der erkannten Münzen
        return circles

    @staticmethod
    def __getColor(circles, image):
        def swapAxis(circles)->np.array:
            swapedAxes = []
            for element in circles:
                element = element[0]
                swapedAxes.append((element[1], element[0], element[2]))
            return np.array(swapedAxes)


        return None


if __name__ == '__main__':
    HufftransformCounter.run(path='../testimages/0.png')
