#-----------------------------------#
import config
from datetime import datetime
#-----------------------------------#
ROI_LINE_X=config.ROI_LINE_X
ROI_LINE_Y=config.ROI_LINE_Y
roi=config.ROI
cooldown=config.COOL_DOWN
#-----------------------------------#
class Event:
    def __init__(self,event_type,confidence,bbox,timestamp,frame=None):
        self.event_type=event_type
        self.confidence=confidence
        self.bbox=bbox
        self.timestamp=timestamp
        self.frame=frame
#-----------------------------------#
class EventEngine:
    def __init__(self):
        #self.cooldown=config.COOL_DOWN #COOL-DOWN
        self.last_activated=None           #COOL-DOWN,timedelta格式以none初始化,不是毫秒
        self.atleast_one_intruder=False ### 记录全局的intrusion pivot
    
    def is_in_ROI(self,bbox): ##bool
        rx1,ry1,rx2,ry2=roi #ROI
        x1,y1,x2,y2=bbox #target
        #return (x1<=rx2 and x2>=rx1 and y1<=ry2 and y2>=ry1)
        if (x1<=rx2 and x2>=rx1 and y1<=ry2 and y2>=ry1):
            return 1.0
        else:
            return 0.0
    
    def cal_overlap_rate(self,bbox): ##float
        ret = 0.0
        rx_left,ry_high,rx_right,ry_low=roi #ROI
        x_left,y_high,x_right,y_low=bbox    #bbox

        # ver-1
        # # not in
        # #if (x_right<rx_left or x_left>rx_right) and (y_high<ry_low or y_low>ry_high) : 
        # if (x_right<rx_left or x_left>rx_right) or (y_high<ry_low or y_low>ry_high) : 
        #     return ret
        # # overlapped
        # w = min(rx_right,x_right)-max(rx_left,x_left)
        # h = min(ry_high,y_high)-max(ry_low,y_low)
        # s = w*h
        # ret = s / ((ry_high-ry_low)*(rx_right-rx_left))

        # ver fixed: still>> bbox_area too big
        intersection_width = max(
            0,
            min(rx_right, x_right) - max(rx_left, x_left)
        )
        intersection_height = max(
            0,
            min(ry_low, y_low) - max(ry_high, y_high)
        )
        intersection_area = intersection_width * intersection_height
        bbox_area = (x_right - x_left) * (y_low - y_high)

        ret = intersection_area / bbox_area
        return ret

    def verify(self,targets,frame=None):
        events = []
        newly_intruded = False ### 记录当前帧的局部intrusion pivot

        for tar in targets:
            if tar.state=="EXPIRED":
                continue

            bbox=tar.bbox
            confidence=tar.confidence

            overlap_rate = self.is_in_ROI(bbox) ###cal_overlap_rate()修正分母前就用这个了

            if self.atleast_one_intruder is True:
                ##ROI内已有intruder
                if overlap_rate > config.EXIT_THRESHOLD: ##在阈值中间带 仅保持intrusion状态 不触发动作
                    newly_intruded = True
                # else: newly_intruded = False   ##低于exit阈值 保持默认的false
            else:
                ##ROI内没有任何intrusion
                if overlap_rate >= config.ENTER_THRESHOLD: ##超过enter阈值
                    newly_intruded = True

                    #if self.atleast_one_intruder is False:###全局状态从无到有>>触发 #这个条件判断可以省略
                    cur=datetime.now()#f"{datetime.now():%H:%M:%S}"
                    if self.last_activated is None or (cur-self.last_activated).total_seconds()>=cooldown:  #COOL-DOWN
                        self.last_activated = cur           #COOL-DOWN
                        e = Event(
                            event_type="intrusion",
                            confidence=confidence,
                            bbox=bbox,
                            timestamp=cur,
                            frame=frame
                        )
                        events.append(e)

        self.atleast_one_intruder=newly_intruded

        return events
