#-----------------------------------#
import config
#-----------------------------------#
ROI_LINE_X=config.ROI_LINE_X
    #MIN_CONF=config.CONF_THRESHOLD
#-----------------------------------#

class EventEngine:

    #def __init__(self):
    #    return self
        
    def is_intruded(self,detections):
        events = []

        for confidence,bbox in detections:
            x1,y1,x2,y2=bbox
            target_center_x=(x1+x2)//2
            if target_center_x<=ROI_LINE_X:
                events.append("intrusion")

        return events
