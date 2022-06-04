import cv2.cv2

from lib import Coinimage
from skimage import io
import glob





def predict(image):
    return 10

'''
@:param image where to count the money
'''
def process(image):  # rückgabe Geldwert in cent zBsp.
    img = Coinimage(image)
    img = img.invert(img)
    img = img.discreteContrast(img)
    img  = img.highContrastToBinary(img)
    img = img.sequentialLabeling(img)
    img = img.countAreaSize(img)
    return predict(img)



def existing_images():
    extensions = ['png']
    files = []
    for file in glob.glob("*." + extensions[0]):


    imagesList = [cv2.cv2.imread(file)for file in files]

    for image in imagesList:
        print(f"Es wurden {process(image)} Cent gezählt")


def with_cam():
    pass

# alle Cents zählen
def count():
    pass

if __name__ == '__main__':
    existing_images()
