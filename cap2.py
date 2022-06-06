import numpy as np
import cv2
import time

exposure = -4
gain = 0
brightness = 0
contrast = 0
tone = 255
whitebalance = 0

exposure2 = -6
gain2 = 20
brightness2 = 190
contrast2 = 255
tone2 = 0
whitebalance2 = 0

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Could not find device.')
    exit()
# cap.set(17, 10000)
counter = 0
name ='test'
print('Brightness:' + str(cap.get(10)))
print('Contrast:' + str(cap.get(11)))
print('Gain:' + str(cap.get(14)))
print('Exposure:' + str(cap.get(15)))
print('White balance:' + str(cap.get(17)))
while(True):
    ret, frame = cap.read()
    # frame = cv2.blur(frame,(7,7),0)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('s'):
        cap.set(15, exposure)
        cap.set(14, gain)
        cap.set(10, brightness)
        cap.set(11, contrast)
        cap.set(12, tone)
        cap.set(17, whitebalance)
        time.sleep(0.5)
        ret, frame = cap.read()
        cv2.imwrite(f'reference/lowContrast/{name}{counter}.png', frame)
        cap.set(15, exposure2)
        cap.set(14, gain2)
        cap.set(10, brightness2)
        cap.set(11, contrast2)
        cap.set(12, tone2)
        cap.set(17, whitebalance2)
        time.sleep(0.5)
        ret, frame = cap.read()
        cv2.imwrite(f'reference/highContrast/{name}{counter}.png', frame)
        counter += 1
    elif cv2.waitKey(1) & 0xFF == ord('n'):
        name = input('Name:\n')
        counter = 0
    elif cv2.waitKey(1) & 0xFF == ord('b'):
        cap.set(10, int(input('Brightness (0 - 255):\n')))
    elif cv2.waitKey(1) & 0xFF == ord('c'):
        cap.set(11, int(input('Contrast (0 - 255):\n')))
    elif cv2.waitKey(1) & 0xFF == ord('g'):
        cap.set(14, int(input('Gain (0 - 255):\n')))
    elif cv2.waitKey(1) & 0xFF == ord('e'):
        cap.set(15, int(input('Exposure (-1 to -7):\n')))
    elif cv2.waitKey(1) & 0xFF == ord('w'):
        cap.set(17, int(input('Whitebalance (-1 to 10000):\n')))
cap.release()
cv2.destroyAllWindows()