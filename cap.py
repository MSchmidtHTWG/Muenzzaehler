import numpy as np
import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Could not find device.')
    exit()
# cap.set(17, 10000)
counter = 0
name ='1Euro'
while(True):
    ret, frame = cap.read()
    # frame = cv2.blur(frame,(7,7),0)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f'{name}{counter}.png', frame)
        counter += 1
cap.release()
cv2.destroyAllWindows()