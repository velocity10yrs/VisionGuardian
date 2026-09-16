import cv2
from ultralytics import YOLO
#from logger import append_log
#from actions import generate_ssname
#from actions import triggered_warning
import events
import actions
import config
import datetime
#-----------------------------------#
TARGET_CLASS="person"
roi=config.ROI
MIN_CONF=config.CONF_THRESHOLD
LOG_FILE=config.LOG_DIR
MODEL_PATH=config.MODEL_PATH
res=None

#-----------------------------------# 一帧中的一个检测结果
class Detection:
    def __init__(self,bbox=(0,0,0,0),conf=0.0):
        self.bbox=bbox
        self.confidence=conf

#-----------------------------------# 系统持续关注的一个现实世界对象
class Target:
    def __init__(self,bbox=(0,0,0,0),conf=0.0,last_seen=0,state=""):
        self.id=0
        self.bbox=bbox
        self.confidence=conf
        self.last_seen=last_seen
        self.state=state

#-----------------------------------# 检测器
class Detector:

    def __init__(self): #init+self
        #model loading
        self.model=YOLO(MODEL_PATH) 

    def detect(self,frame):
        detections = []
        #draw ROI
        rx1,ry1,rx2,ry2=roi
        cv2.rectangle(frame,                     
             (rx1,ry1),
             (rx2,ry2),
             (0,0,255),
             2)
    
        results=self.model.predict(frame,conf=MIN_CONF,verbose=False)
            #print("using model:",self.model)#debug
        res=results[0]
            #debug
            #cls=int(res.boxes.cls[0])
            #print(res.names[cls])
        for box in res.boxes:
              cls=int(box.cls)
              name=res.names[cls]
              if(name==TARGET_CLASS):
                    confidence=float(box.conf)
                    xyxy=tuple(map(int,box.xyxy[0])) #map返回的是迭代器
                    #draw target
                    x1,y1,x2,y2=xyxy
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.putText(frame,name,(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
                    #detections append
                    new_dect = Detection(xyxy,confidence)
                    #detections.append( (confidence,xyxy,frame) )
                    detections.append(new_dect)
        return detections
