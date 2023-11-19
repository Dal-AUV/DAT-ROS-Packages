# start up the orange tape detection program
# date: Oct 22, 2023
# updated: Oct 29, 2023
#          finish the first step, be able to detect orange objects, adding the contour with the label
import cv2
from matplotlib import pyplot as plt
import numpy as np
import time

#capture the video from source, 0: connecting to the default camera
cap = cv2.VideoCapture(0)
while True:
    #whether the frame was successfully read
    ret, frame = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define upper and lower bound for the colour orange
    lower_limit =np.array([0,150,150])
    upper_limit =np.array([15,255,255])
    #generate the mask
    orangemask = cv2.inRange(hsv, lower_limit, upper_limit)
    orange = cv2.bitwise_and(frame, frame, mask=orangemask)
    edges = cv2.Canny(orange, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    # Creating contour to track orange color
    _,contours,_ = cv2.findContours(orangemask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            cx, cy = x + w // 2, y + h // 2  # Calculate the center of the bounding box
            imageFrame = cv2.rectangle(frame, (x, y),
                                       (x + w, y + h),
                                       (0, 0, 255), 2)

            cv2.putText(imageFrame, "Orange Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))
            # Draw a line through the center of the bounding box
            cv2.line(frame, (cx, y), (cx, y + h), (255, 0, 0), 2)
            cv2.line(frame, (x, cy), (x + w, cy), (255, 0, 0), 2)

            # Calculate the angle of the line
            #angle = np.degrees(np.arctan2(h, w))

            # Print or use the center line coordinates and angle
            #print(f"Center Line Coordinates: ({cx}, {cy}), Angle: {angle:.2f}")

            # Fit a rotated rectangle around the contour
            rect = cv2.minAreaRect(contour)
            center, size, angle = rect

            # Convert the angle to be in the range [0, 180)
            if size[0] < size[1]:
                angle += 90

            # Draw the rotated rectangle
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
            # Calculate the angle of the line
            print(f"Center Line Coordinates: ({center[0]:.2f},{center[1]:.2f}), Angle: {angle:.2f}")


    cv2.imshow('Original', frame)  # to display the original frame
    cv2.imshow('orange Detector', orange)  # to display the blue object output
    cv2.imshow('Edges', edges)# To display the edges of the orange object
    #loop terminated when pressed q
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
#clean up
cap.release()
cv2.destroyAllWindows()