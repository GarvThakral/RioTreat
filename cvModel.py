import cv2 as cv
import ultralytics
import supervision as sv
from ultralytics import YOLO
import serial
import time
from threading import Timer
model = YOLO("yolo11n.pt")


last = 0

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1) 
def write_read(x): 
    arduino.write(bytes(x, 'utf-8')) 
    time.sleep(0.05) 
    data = arduino.readline() 
    return data 

IPHONE_URL = "http://admin:admin@192.168.29.133:8081/video"


capture = cv.VideoCapture(IPHONE_URL)
capture.set(cv.CAP_PROP_OPEN_TIMEOUT_MSEC, 60000)  # 60 second timeout
capture.set(cv.CAP_PROP_READ_TIMEOUT_MSEC, 60000)   # 60 second read timeout
frameIndex = 0

def detectedFalse(detected):
    detected[0] = False
    return detected[0]

detected = [False]

while(True):
    frameIndex +=1 
    isFrame , frame = capture.read()
    result = model(frame,conf = 0.5,classes = 16 , verbose = False)[0]
    detections = sv.Detections.from_ultralytics(result)
    if not detected[0]:
        if(len(detections) > 0):
            detected = [True]
            r = Timer(4.0, detectedFalse , [detected])
            r.start()
            frame = cv.putText(frame,"Rio Detected",(100,100),cv.FONT_HERSHEY_COMPLEX,1.0,(0,255,0),2)
            if detected:
                frame = cv.putText(frame,"Detected",(100,300),cv.FONT_HERSHEY_COMPLEX,1.0,(0,255,0),2)
            if last == 0:
                data = write_read("180")
                last = 180
            else:
                data = write_read("0")
                last  = 0
        else:
            frame = cv.putText(frame,"Not Detected",(200,100),cv.FONT_HERSHEY_COMPLEX,1.0,(0,255,0),2)
    else:
        frame = cv.putText(frame,"Rio Detected",(100,100),cv.FONT_HERSHEY_COMPLEX,1.0,(0,255,0),2)
        frame = cv.putText(frame,"Detected",(100,300),cv.FONT_HERSHEY_COMPLEX,1.0,(0,255,0),2)


    if not isFrame:
        break
    cv.imshow("Video",frame)
    if cv.waitKey(25) & 0xFF == ord('q'):
        break