#-----------------------------------#
import config
#-----------------------------------#
ROI_LINE_X=config.ROI_LINE_X
#-----------------------------------#

class Event:
    def __init__(self,event_type,detection):
        self.event_type=event_type
        self.detection=detection

    def detection(self,detections):
        events = []

        for confidence,bbox,frame in detections:
            x1,y1,x2,y2=bbox
            target_center_x=(x1+x2)//2
            
            if target_center_x<=ROI_LINE_X:
                e = Event("intrusion",
                        (confidence,bbox,frame)
                )
                events.append(e)

        return events
