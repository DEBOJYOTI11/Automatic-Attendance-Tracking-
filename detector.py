import cv2,os
import numpy as np
from PIL import Image
import pickle
import sqlite3
import time
facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
rec=cv2.createLBPHFaceRecognizer();
rec.load("RECOGNIZER/trainingdata.yml")
path = 'DATASET'

from time import gmtime, strftime

def checkDate(database, current , threshold =15):
    
    d = database.split(" ")[0]
    d2 = current.split(" ")[0]
    t = database.split(" ")[1]
    t2 = current.split(" ")[1]

    print d,d2
    if(d!=d2):
        return True

    t = t.split(":")
    t2 = t2.split(":")
    print t[0], t2[0]
    if(t[0]==t2[0]):
        return False
    return True if int(t[0])-int(t[1]) >threshold else False

    
def getProfile(id):
    connection=sqlite3.connect("Students Database.db")
    conn = connection.cursor()
    cmd="SELECT * FROM StudentA WHERE ID="+str(id)
    conn.execute(cmd)
    cursor = conn.fetchall()

    profile=[]
    for row in cursor:
        profile.append(row)

        
    if(len(profile)>1):
            print  "[Warning] Fatal error .Error in datbase, more then one record found with same ID"
            sys.exit(1)

    if(len(profile)==0):
        profile = None
        return profile

    profile = profile[0]
    #print 'Before: ',profile
    last_attended = profile[-2]
    if(checkDate(last_attended, strftime( "%Y-%m-%d %H:%M:%S",gmtime()))):
        
        cmd = "update StudentA set lastSeen  =\"%s\" , attendenceCount = attendenceCount+1 where id =%d"%(strftime( "%Y-%m-%d %H:%M:%S",gmtime()),id)
        conn.execute(cmd)
        print '[info] updated attendence'
        cmd  = "select * from StudentA where id = "+str(id)
        conn.execute(cmd)
        conn = conn.fetchall()
        print '[Success] Current attendence is %d'%(conn['attendence'])
    else:
        print '[warning] Student seen int the same day!'
    connection.commit()
    connection.close()
    return profile

camera = cv2.VideoCapture(0)
font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)


while True:
    ret, img=camera.read()
    #img = cv2.imread("test/im2.jpg", 0)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    
    #for undected faces
    #tup = (0,0,img.shape[0],img.shape[1])
    #faces = faces +(tup,)

    for(x,y,w,h) in faces:
        id, conf = rec.predict(gray[y:y+h,x:x+w])
        cv2.rectangle(img, (x,y),(x+w,y+h) , (255,0,0),2)
        #print  '[info] Id of the face is %d with confidence %d'%(id,conf)
        profile=getProfile(id)
        print conf
        #print 'detail about person ',profile
        if(profile is None or conf<40):
            profile = [0,"Unknown","NA","NA","NA"]
            print "Student not found in database!!!"
        
        cv2.cv.PutText(cv2.cv.fromarray(img),"NAME:"+str(profile[1]),(x,y+h+30),font, (0,128,0))
        cv2.cv.PutText(cv2.cv.fromarray(img),"ROLLNO:"+str(profile[2]),(x,y+h+60),font, (0,128,0))
        cv2.cv.PutText(cv2.cv.fromarray(img),"GENDER:"+str(profile[3]),(x,y+h+90),font, (0,128,0))
        cv2.cv.PutText(cv2.cv.fromarray(img),"DEPARTMENT:"+str(profile[4]),(x,y+h+120),font, (0,128,0))
            # cv2.cv.PutText(cv2.cv.fromarray(img),"BATCH:"+str(profile[5]),(x,y+h+150),font, 255)
            # cv2.cv.PutText(cv2.cv.fromarray(img),"BATCH:"+str(profile[6])+str(1),(x,y+h+150),font, 255)
            
    
    cv2.imshow("FACE",img)
    k = cv2.waitKey(100)
    
    if k==27:
        cv2.destroyAllWindows()
        break
    
print  '[Info] Exiting'
