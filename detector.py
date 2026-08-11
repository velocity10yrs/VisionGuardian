import cv2
from ultralytics import YOLO
from logger import append_log
from actions import generate_ssname
from actions import triggered_warning
#-----------------------------------#
ROI_LINE_X=540
MIN_CONF=0.25
TARGET_CLASS="person"
LOG_FILE="logs/detector.log"
res=None
last_warning=None
#-----------------------------------#
class Detector:
    def detect(self,frame):
        model=YOLO("model/yolo11n.pt")
        last_warning = False

        while True:
            #预测
            results=model.predict(frame,conf=MIN_CONF,verbose=False)
            res=results[0]
            #ROI
            cv2.line(frame,
                    (ROI_LINE_X,0),(ROI_LINE_X,frame.shape[0]),
                    (0,0,255),2)
            #ROI判断
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
                #事件:INTRUSION警报
                warning = (cen_x<=ROI_LINE_X)
                    #last_warning = False #opt
                #动作:warning驱动
                if warning and not last_warning:
                    last_warning=warning #只报警新目标
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
                last_warning=warning; #fix:一旦退出再进入需要重新报警 