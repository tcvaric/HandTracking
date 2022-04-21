import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

width, height = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

#Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

#communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5010)

while True:
    #Webcam
    success, img = cap.read()

    #Hands
    hands, img = detector.findHands(img)

    data = []
    #Landmark values - (x,y,z)*21
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        #print(lmList)
        for lm in lmList:
            data.extend([lm[0], height - lm[1], lm[2]])
        #print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)

    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()