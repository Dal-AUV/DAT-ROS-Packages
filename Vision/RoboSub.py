import cv2 
import numpy as np

class challenge:


    #simple function for testing purposes
    def ShowImageInColour(self, path):
        
        img = cv2.imread(path)
        cv2.imshow("Colour Image", img)
        cv2.waitKey(0)
    
    #centroid function - can return x,y centroid data?
    def DisplayCentroidLocation(self):
        cap = cv2.VideoCapture(0)

        while True:
            #success is the return value to tell us abt the frames in the video
            success, frame = cap.read()
            width = int(cap.get(3))
            height = int(cap.get(4))
            #convert frame into hsv values
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            #define upper and lower bound for the colour blue
            lower_blue = np.array([100, 100, 0])   #110, 50, 50 is default
            upper_blue = np.array([130, 255, 255])
            #generate the mask
            mask = cv2.inRange(hsv,lower_blue, upper_blue)
            #creates image with only blue within bound
            result = cv2.bitwise_and(frame, frame, mask=mask) #bitwise and is to blend frame with frame using mask to only give us the pixels we care about 

            #implementing centroiod
            grey_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(grey_image,127,255,0)
            moment = cv2.moments(thresh)
            try:
                centroidX = int(moment["m10"] / moment["m00"])
                centroidY = int(moment["m01"] / moment["m00"])
                cv2.circle(result, (centroidX, centroidY), 5, (255, 255, 255), -1)
                cv2.putText(result, "Centroid", (centroidX - 25, centroidY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            except:
                cv2.putText(result, "Centroid is lost!",(75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

            #show images
            cv2.imshow("Frame", frame)
            cv2.imshow("Result", result)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


