#import packages

from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os

#arguemnt parser
#ap = argparse.ArgumentParser()
#ap.add_argument("-c", "--cascade", required=True, help = "path to face cascade")
#ap.add_argument("-o", "--output", required=True, help = "path to output directory")
#args = vars(ap.parse_args())

def gather():
    args = {"cascade" : "haarcascade_frontalface_default.xml", "output" : "test"}
    #load opencv's haar cascade for face detection
    detector = cv2.CascadeClassifier(args["cascade"])
    
    #initialize video stream for camera sensor to warm up. Initialize total num of example
    print("[INFO] starting, les get dis bread fam...")
    
    #changes based on which camera being used 
    #vs = VideoStream(src=0).start()
    vs = VideoStream(usePiCamera=True).start()
    
    #allow camera time to warm up
    time.sleep(2.0)
    total = 0
    
    #loop over frames from video stream
    while True:
        #grab frame from threaded video stream and clone it. (in case writing to disk) and resize to frame for faster detection
        frame = vs.read()
        orig = frame.copy()
    
        #resize image to for easier recognition
        frame = imutils.resize(frame, width = 400)
    
        #detect faces in grayscale frame. 
        #scaleFactor = specifies how much image size is reduced at each image scale
        #minNeighbors = how many neighbors each candidate rectangle should have to retain
        #min size, minium possible object size (face)
        rects = detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
        
        #loop over face detections and draw them on the fram
        for (x, y, w, h) in rects:
            cv2.rectangle(img = frame, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)
    
        #show output frame to screen
        cv2.imshow("Frame", frame)
    
        key = cv2.waitKey(1) & 0xFF
    
        # if k is pressed, write original image to disk to process later for face recognitition
        if key == ord("k"):
            #zfill left pads with 0 
            p = os.path.sep.join([args["output"], "{}.png".format(str(total).zfill(5))])
            cv2.imwrite(p, orig)
            print("picture was takizzled")
            total += 1
    
        #if the q is pressed, break from loop
        elif key == ord("q"):
            break
    
    #print total number of faces saved and clean up
    print("[INFO] eyy, we saved {} faces".format(total))
    print("[INFO] cleaning up")
    cv2.destroyAllWindows()
    vs.stop()
    
