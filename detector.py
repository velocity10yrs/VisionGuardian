import cv2
from ultralytics import YOLO
import config
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
        res=results[0]

        for box in res.boxes:
              cls=int(box.cls)
              name=res.names[cls]
              if(name==TARGET_CLASS):
                    confidence=float(box.conf)
                    xyxy=tuple(map(int,box.xyxy[0])) 

                    #draw target
                    x1,y1,x2,y2=xyxy
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.putText(frame,name,(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

                    new_dect = Detection(xyxy,confidence)
                    detections.append(new_dect)
        return detections
