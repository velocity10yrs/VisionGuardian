"""
系统持续关注的一个现实世界对象
"""
import config
import math
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
        last_y = (last_tar.bbox[1]+last_tar.bbox[3])//2
        last_x = (last_tar.bbox[0]+last_tar.bbox[2])//2

        cur_y  = (new_tar.bbox[1]+new_tar.bbox[3])//2
        cur_x  = (new_tar.bbox[0]+new_tar.bbox[2])//2

        dist_sqrt = math.pow(cur_y-last_y,2)+math.pow(cur_x-last_x,2)
        return dist_sqrt

    def update_target(self,target,tar,now): #void
        target.bbox=tar.bbox
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
