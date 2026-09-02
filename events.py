#-----------------------------------#
import config
from datetime import datetime
#-----------------------------------#
ROI_LINE_X=config.ROI_LINE_X
#-----------------------------------#

class Event:
    def __init__(self,event_type,confidence,bbox,timestamp):
        self.is_intruded=False
        self.event_type=event_type
        self.confidence=confidence
        self.bbox=bbox
        self.timestamp=timestamp

class EventEngine:
    def detect(self,detections):
        events = []

        for confidence,bbox in detections:
            x1,y1,x2,y2=bbox
            target_center_x=(x1+x2)//2
            
            if target_center_x<=ROI_LINE_X:
                if self.is_intruded is False:
                    cur=datetime.now()#f"{datetime.now():%H:%M:%S}"
                    e = Event(
                        event_type="intrusion",
                        confidence=confidence,
                        bbox=bbox,
                        timestamp=cur
                    )
                    events.append(e)
                self.is_intruded=True
            else:
                self.is_intruded=False

        return events
