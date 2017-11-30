import cv2
import numpy as np
import sqlite3

facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
camera=cv2.VideoCapture(0);

def insertOrUpdate(data):
    id = data[0]
    name = data[1]
    connection=sqlite3.connect("Students Database.db")
    conn = connection.cursor()
    
    cmd="SELECT * FROM StudentA WHERE id="+str(id)

    conn.execute(cmd)
    result = conn.fetchall()
    
    isRecordExist=0
    for row in result:
        print row
        isRecordExist=1

    if(isRecordExist==1):
        cmd="UPDATE StudentA SET name=\""+str(name)+"\" WHERE id="+str(id)
    else:
        #cmd="INSERT INTO StudentA Values("+str(Id)+","+str(Name)+","+rest[0]+','+rest[1]+','+rest[2]+','+rest[3]+','rest[4]+")"
        cmd= "insert into StudentA values(%d,\"%s\",\"%s\",\"%s\",\"%s\",datetime(\"now\"),%d)"%(data[0],data[1],data[2],data[3],data[4],data[6])
        print "[Info] : Student record added as %d | %s"%(id,name)
    
    conn.execute(cmd)
    connection.commit()
    connection.close()

while 1:
    id=raw_input('Enter your Roll NO :')
    name=raw_input('Enter your Name:')
    data = [int(id),name, "CSBX","M", "CSE","datetime()",1]

    insertOrUpdate(data)
    samplenumber=0

    while(True):
        ret,img=camera.read();
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);
        faces=facedetect.detectMultiScale(gray,1.3,5)
        for(x,y,w,h) in faces:
            samplenumber=samplenumber+1;
            cv2.imwrite("DATASET/User."+str(id)+"."+str(samplenumber)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        cv2.imshow("FACE",img)
        cv2.waitKey(100)
        if(samplenumber>20):
            camera.release()
            cv2.destroyAllWindows()
            break
