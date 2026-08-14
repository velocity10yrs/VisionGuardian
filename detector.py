import cv2
from ultralytics import YOLO
from logger import append_log
from actions import generate_ssname
from actions import triggered_warning
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
def ROI(frame,res):
    #roi划定
    cv2.line(frame,
            (ROI_LINE_X,0),(ROI_LINE_X,frame.shape[0]),
            (0,0,255),2)
    #intrusion判断
    for box in res.boxes:
                cls=int(box.cls)
                name=res.names[cls] #fix
                if(name!=TARGET_CLASS): continue
                #
                x1,y1,x2,y2=map(int,box.xyxy[0])
                cen_x=(x1+x2)//2;cen_y=(y1+y2)//2
                cv2.circle(frame,
                        (cen_x,cen_y),
                        5,(255,0,0),-1)
    return (cen_x,cen_y),(x1,y1,x2,y2)
def is_intruded(cen_x,ROI_LINE_X):
    return cen_x<=ROI_LINE_X
def triggered_warning():#解耦
    print(f"[{datetime.now():%H:%M:%S}] Warning: person entered ROI.") 
def generate_ssname():#解耦
    return datetime.now().strftime("%Y%m%d_%H%M%S")+".jpg" 
def action(warning,frame,roi):
    if warning and not last_warning:
                last_warning=warning #只报警新目标
                x1,y1,x2,y2=roi
                cv2.rectangle(frame,
                            (x1,y1),(x2,y2),
                            (255,0,0),2)
                cv2.putText(frame,"WARNING",
                            (30,50),cv2.FONT_HERSHEY_SIMPLEX,
                            1,(0,0,255),3)
                triggered_warning()
                ss_name=generate_ssname()
                #动作:logging+sshot
                append_log(ss_name)
#-----------------------------------#
class Detector:
    def detect(self,frame):
        person_detected = False
        model=YOLO(MODEL_PATH)
        
        #model
        results=model.predict(frame,conf=MIN_CONF,verbose=False)
        res=results[0]
        for box in res.boxes:
              cls=int(box.cls)
              name=res.names[cls]
              if(name==TARGET_CLASS):
                    person_detected=True
        return person_detected
        
        ##ROI+intrusion
        #res=ROI(frame,res)
        #cen_x,cen_y=res[0]
        #x1,y1,x2,y2=res[1]

        ##triggers
        #last_warning = False
        #warning=is_intruded(cen_x,ROI_LINE_X)
                
        ##actions
        #action(warning,frame,res[1])
        #last_warning=warning; 