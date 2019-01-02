from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os 

# construct arg parser and parse
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
    help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
    help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
    help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())



# Grab Paths to input images
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))
 
# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

for (i, imagePath) in enumerate(imagePaths):
    # extract person name from image path
    print("[INFO] processing image {}/{}".format(i + 1,
        len(imagePaths)))
    name = imagePath.split(os.path.sep)[-2]
    print(imagePath)

    # Convert loaded image from BGR to RGB
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
    # detect (x, y) coordinates of bounding boxes
    boxes = face_recognition.face_locations(rgb, 
        model=args["detection_method"])

    # compute facial embeddings 
    encodings = face_recognition.face_encodings(rgb, boxes)
    
    # loop over encodings
    for encoding in encodings:
        # add each encoding + name to set of known names & values
        knownEncodings.append(encoding)
        knownNames.append(name)



    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open(args["encodings"], "wb")
    f.write(pickle.dumps(data))
    f.close()

    

    
