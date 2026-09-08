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
ROI_LINE_X=config.ROI_LINE_X
MIN_CONF=config.CONF_THRESHOLD
LOG_FILE=config.LOG_DIR
MODEL_PATH=config.MODEL_PATH
res=None
#-----------------------------------#
# def ROI(frame,res):
#     #roi划定
#     cv2.line(frame,
#             (ROI_LINE_X,0),(ROI_LINE_X,frame.shape[0]),
#             (0,0,255),2)
#     #intrusion判断
#     for box in res.boxes:
#                 cls=int(box.cls)
#                 name=res.names[cls] #fix
#                 if(name!=TARGET_CLASS): continue
#                 #
#                 x1,y1,x2,y2=map(int,box.xyxy[0])
#                 cen_x=(x1+x2)//2;cen_y=(y1+y2)//2
#                 cv2.circle(frame,
#                         (cen_x,cen_y),
#                         5,(255,0,0),-1)
#     return (cen_x,cen_y),(x1,y1,x2,y2)
##def is_intruded(cen_x,ROI_LINE_X):
##    return cen_x<=ROI_LINE_X
##def triggered_warning():#解耦
##    print(f"[{datetime.now():%H:%M:%S}] Warning: person entered ROI.") 
##def generate_ssname():#解耦
##    return datetime.now().strftime("%Y%m%d_%H%M%S")+".jpg" 
#-----------------------------------#
# def action(warning,frame,roi):
#     if warning and not last_warning:
#                 last_warning=warning #只报警新目标
#                 x1,y1,x2,y2=roi
#                 cv2.rectangle(frame,
#                             (x1,y1),(x2,y2),
#                             (255,0,0),2)
#                 cv2.putText(frame,"WARNING",
#                             (30,50),cv2.FONT_HERSHEY_SIMPLEX,
#                             1,(0,0,255),3)
#                 triggered_warning()
#                 ss_name=generate_ssname()
#                 #动作:logging+sshot
#                 append_log(ss_name)
#-----------------------------------#
class Detector:

    def __init__(self): #init+self
        #model loading
        self.model=YOLO(MODEL_PATH) 

    def detect(self,frame):
        detections = []
        #draw ROI
        cv2.line(frame,                     
             (ROI_LINE_X,0),
             (ROI_LINE_X,frame.shape[0]), #bug:frame.shape[1]
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
                    detections.append( (confidence,xyxy) )
        return detections
