# start up the orange tape detection program
# date: Oct 22, 2023
# updated: Oct 29, 2023
#          finish the first step, be able to detect orange objects, adding the contour with the label
import cv2
from matplotlib import pyplot as plt
import numpy as np

#capture the video from source, 0: connecting to the default camera
cap = cv2.VideoCapture(0)
while True:
    #whether the frame was successfully read
    ret, frame = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define upper and lower bound for the colour orange
    lower_limit =np.array([0,100,100])
    upper_limit =np.array([30,255,255])
    #generate the mask
    orangemask = cv2.inRange(hsv, lower_limit, upper_limit)
    orange = cv2.bitwise_and(frame, frame, mask=orangemask)
    # Creating contour to track orange color
    _,contours,_ = cv2.findContours(orangemask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(frame, (x, y),
                                       (x + w, y + h),
                                       (0, 0, 255), 2)

            cv2.putText(imageFrame, "Orange Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))


    cv2.imshow('Original', frame)  # to display the original frame
    cv2.imshow('orange Detector', orange)  # to display the blue object output
    #loop terminated when pressed q
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
#clean up
cap.release()
cv2.destroyAllWindows()