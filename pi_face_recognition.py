from imutils.video import VideoStream
from imutils.video import FPS
#from multiprocessing import Process
import playtheme
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

#cv2.destroyAllWindows()
#vs.stop()

UNKNOWN = "Unknown"
counter = 0

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required = True,
    help = "path where the face cascade resides")
ap.add_argument("-e", "--encodings", required = True,
    help = "path to serialized db of facial encodings")
args = vars(ap.parse_args())

#load known faces and embeddings along with OpenCV's Haar
#cascade for face detection
print("[INFO] loading encodings + face detection")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])

#intialize video stream and allow camera sensor to warm up
print("[INFO] start video stream...")
#vs = VideoStream(src=0).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

#start the FPS counter
fps = FPS().start()

#loop video file stream
while True:
    #grab the frame and resize to 
    frame = vs.read()
    frame = imutils.resize(frame, width = 400)

    #convert the input frame from (1) BGR to gray scale 
    #BGR to RGB for race recognition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #detect faces in the grayscale fram
    rects = detector.detectMultiScale(gray, scaleFactor = 1.1,
        minNeighbors=5, minSize=(30,30))
    
    #openCV returns bounding box coordinates in (x, y, w, h)
    #but we need in (top, right, bottom, left)
    boxes = [(y, x+w, y+h, x) for (x, y ,w, h) in rects]
    print("boxes ")
    print(boxes)
   
    #if no face returned in rects, then face_encodings does nothing
    #compute facial embeddings for each face bounding box
    
    ###TODO CHECK IF STILL RUNS ENCODING WITH NO FACES###
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    #loop over facial embeddings
    for encoding in encodings:
        #match face in the input image to our known encodings
        matches = face_recognition.compare_faces(data["encodings"],
            encoding)
        name = UNKNOWN
        
        #  check to to see if we found a match
        if True in matches:
            #find the indexes of all matched faces then initialize a 
            #dictionary to cout number of times face was matched
            
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            #loop over matched indexes and maintain a count for each
            #recognized face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            
            # determine the reconizedface with largest number
            # of nodes
            name = max(counts, key=counts.get)
            if name == "Nelson": 
                counter+=1
            if name == "Jesse": 
                counter+=1
            if name == "Sang": 
                counter+=1


        #update the list of names
        names.append(name)
    ##loop over recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 0), 2)
        y = top -15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 
            0.75, (0, 255, 0), 2)
    
    print("updating fps")
    
    if counter == 2:
        playtheme.playTheme(name)
        #name = "Nelson"

    
    #display the image to our sreen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    #


    ##if the q is pressed, break from loop
    if key == ord("q"):
        break

    fps.update()

#stop the time and display FPS info
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

#clean up
cv2.destroyAllWindows()
vs.stop()
