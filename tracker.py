"""
系统持续关注的一个现实世界对象
"""
import config
import math
from collections import deque
from datetime import datetime 
#-----------------------------------# 

STATE_ACTIVE="ACTIVE"
STATE_MISSING="MISSING"
STATE_EXPIRED="EXPIRED"

#-----------------------------------# 被管理对象
class Target:
    def __init__(self,target_id=0,bbox=(0,0,0,0),confidence=0.0,last_seen=0,state=""):
        self.target_id=target_id
        self.bbox=bbox
        self.confidence=confidence
        self.last_seen=last_seen
        self.state=state
        
        self.center_history=deque(maxlen=config.JITTER_HISTORY_SIZE)
        self.center_history.append(self.bbox_center(bbox))

    @staticmethod
    def bbox_center(bbox):
        x1,y1,x2,y2=bbox
        return ((x1+x2)/2,(y1+y2)/2)

    def add_center(self,bbox):
        self.center_history.append(self.bbox_center(bbox))

    def averaged_center(self):
        count=len(self.center_history)
        x_sum=sum(center[0] for center in self.center_history)
        y_sum=sum(center[1] for center in self.center_history)
        return (x_sum/count,y_sum/count)
#-----------------------------------# 管理者
class Tracker:
    def __init__(self):
        self.current_id=0
        self.target_list=[]

    def add(self,tar,now=None): #void
        if now is None:
            now=datetime.now()
        self.current_id+=1
        new_target = Target(self.current_id,
                        tar.bbox,
                        tar.confidence,
                        last_seen=now,
                        state=STATE_ACTIVE)
        self.target_list.append(new_target)

    def cal_dist(self,new_tar,last_tar): #int
        last_x,last_y=last_tar.averaged_center()
        cur_x,cur_y=Target.bbox_center(new_tar.bbox)

        dist_sqrt = math.pow(cur_y-last_y,2)+math.pow(cur_x-last_x,2)
        return dist_sqrt

    def update_target(self,target,tar,now): #void
        target.add_center(tar.bbox)
        avg_x,avg_y=target.averaged_center()
        x1,y1,x2,y2=tar.bbox
        width=x2-x1
        height=y2-y1
        target.bbox=(
            int(round(avg_x-width/2)),
            int(round(avg_y-height/2)),
            int(round(avg_x+width/2)),
            int(round(avg_y+height/2))
        )
        target.confidence=tar.confidence
        target.last_seen=now
        target.state=STATE_ACTIVE         #新发现时=active

    def check(self,tar,now=None): #int
        if now is None:
            now=datetime.now()
        #exist target
        closest_tar=-1
        closest_distsq=float("inf") #init to max
        for index,exist_tar in enumerate(self.target_list):#compare w each exist tar
            if exist_tar.state==STATE_EXPIRED:
                continue
            distsq = self.cal_dist(tar,exist_tar)
            if(distsq<closest_distsq): #update closest
                closest_tar=index                       #无论是新发现，还是STATE_MISSING，都从这里验证是否为已有target
                closest_distsq=distsq
        if(closest_distsq<=config.PERMITTED_RANGE_SQRT): 
            self.update_target(self.target_list[closest_tar],tar,now)
            return closest_tar
        #new target    
        else:
            self.add(tar,now)
            return len(self.target_list)-1
        
    def target_lost_over_time(self,now,target,active_targets):
            missing_time=(now-target.last_seen).total_seconds()   #计算target消失时间

            if missing_time>=config.TARGET_EXPIRE_TIMEOUT_SEC: #不会加入target_list[]
                target.state=STATE_EXPIRED
                return

            if missing_time>=config.TARGET_MISSING_TIMEOUT_SEC: #状态变更
                target.state=STATE_MISSING

            active_targets.append(target)
    
    def refresh_lifecycle(self,matched_indexes,now): #void
        active_targets=[]

        for index,target in enumerate(self.target_list):
            
            if index in matched_indexes:
                active_targets.append(target)
                continue
            
            self.target_lost_over_time(now,target,active_targets)

        self.target_list=active_targets

    def tracking(self,detections,now=None): #target[]
        if now is None:
            now=datetime.now()
        matched_indexes=set()

        for d in detections:
            matched_index=self.check(d,now)
            matched_indexes.add(matched_index)

        self.refresh_lifecycle(matched_indexes,now)
        return self.target_list
#-----------------------------------#
