import cv2
from ultralytics import YOLO
import config
#-----------------------------------#
TARGET_CLASS="person"
interval=config.DETECTION_INTERVAL
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
        self.model=YOLO(MODEL_PATH) 

    def detect(self,frame):
        detections = []

        results=self.model.predict(frame,conf=MIN_CONF,verbose=False)
        res=results[0]

        for box in res.boxes:
            cls=int(box.cls)
            name=res.names[cls]
            if(name==TARGET_CLASS):
                    confidence=float(box.conf)
                    xyxy=tuple(map(int,box.xyxy[0])) 

                    new_dect = Detection(xyxy,confidence)
                    detections.append(new_dect)
        return detections
