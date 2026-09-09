#-----------------------------------#
import cv2
import config
from datetime import datetime
#-----------------------------------#
ROI_LINE_X=config.ROI_LINE_X
ROI_LINE_Y=config.ROI_LINE_Y
roi=config.ROI
#-----------------------------------#

class Event:
    def __init__(self,event_type,confidence,bbox,timestamp,frame):
        #self.is_intruded=False
        self.event_type=event_type
        self.confidence=confidence
        self.bbox=bbox
        self.timestamp=timestamp
        self.frame=frame

class EventEngine:
    def __init__(self):
        self.is_intruded=False
    
    #def passing_frames(frame):
    #    return frame
    
    def is_in_ROI(self,bbox):
        rx1,ry1,rx2,ry2=roi #ROI
        x1,y1,x2,y2=bbox #target
        
        return (x1<=rx2 & y1<=ry2)

    def verify(self,detections):
        events = []

        for confidence,bbox,frame in detections:
            #print(bbox)#debug
            if self.is_in_ROI(bbox):
                #print("in")#debug
                if self.is_intruded is False:
                    cur=datetime.now()#f"{datetime.now():%H:%M:%S}"
                    e = Event(
                        event_type="intrusion",
                        confidence=confidence,
                        bbox=bbox,
                        timestamp=cur,
                        frame=frame
                    )
                    #print("intru")#debug
                    events.append(e)
                    #传帧
                    #self.passing_frames(frame)
                self.is_intruded=True
            else:
                self.is_intruded=False

        return events
