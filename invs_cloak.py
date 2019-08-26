import cv2
import numpy as np

cap = cv2.VideoCapture(0)

#The first live feed is to capture the background without the subject
while True:
    ret, frame = cap.read()
    f = cv2.flip(frame, 1)
    cv2.imshow('result', f)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        break

cap.release()
cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)

#The second live feed is for the actual result. Subject can now enter the feed
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    kernel = np.ones((2,2), np.uint8)  #create a kernel for applying morphology
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    #created an HSV range by trial and error
    lhsv = np.array([115, 100, 150])
    uhsv = np.array([255, 255, 255])

    #create mask based on hsv range
    mask = cv2.inRange(hsv_frame, lhsv, uhsv)

    #apply closing (morphologyex) on the mask to remove the grains in the mask
    clos_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    mask_inv = cv2.bitwise_not(clos_mask)

    #create two results - bitwise and on the normal mask to extract the first feed around the cloth, result1 for bitwise and on the inverted mask to extract the current camera feed
    result = cv2.bitwise_and(f, f, mask=clos_mask)
    result1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    #add both results on top of each other
    r = cv2.add(result, result1)

    #uncomment the next two lines to see the mask and original feed
    #cv2.imshow('frame', frame)
    #cv2.imshow('mask_inv', closing)

    cv2.imshow('result', r)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()