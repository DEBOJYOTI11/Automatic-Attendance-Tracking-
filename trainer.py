import os
import cv2
import numpy as np
from PIL import Image

recognizer=cv2.createLBPHFaceRecognizer();
path='DATASET/'

def getImagesWithID(path):
    imagepaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagepath in imagepaths:
        faceimage=Image.open(imagepath).convert('L');
        facenp=np.array(faceimage,'uint8')
        ID=int(os.path.split(imagepath)[-1].split('.')[1])
        faces.append(facenp)
        IDs.append(ID)
        cv2.imshow("TRAINING",facenp)
        cv2.waitKey(10)
    return IDs, faces

IDs,faces=getImagesWithID(path)
recognizer.train(faces,np.array(IDs))
recognizer.save('RECOGNIZER/trainingdata.yml')
cv2.destroyAllWindows()
        
