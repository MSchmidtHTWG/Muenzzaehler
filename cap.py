import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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
        cv2.imwrite(f'{name}{counter}.png', frame)
        print('Brightness:' + str(cap.get(10)))
        print('Contrast:' + str(cap.get(11)))
        print('Gain:' + str(cap.get(14)))
        print('Exposure:' + str(cap.get(15)))
        print('White balance:' + str(cap.get(17)))
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