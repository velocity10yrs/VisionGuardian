"""
系统持续关注的一个现实世界对象
"""
import config
import detector
import math
from datetime import datetime 
#-----------------------------------# 

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

    def add(self,tar): #void
        self.current_id+=1
        new_target = Target(self.current_id,
                        tar.bbox,
                        tar.confidence,
                        last_seen=datetime.now(),
                            state="DETECTED")
        self.target_list.append(new_target)

    def cal_dist(self,new_tar,last_tar): #int
        last_y = (last_tar.bbox[1]+last_tar.bbox[3])//2
        last_x = (last_tar.bbox[0]+last_tar.bbox[2])//2

        cur_y  = (new_tar.bbox[1]+new_tar.bbox[3])//2
        cur_x  = (new_tar.bbox[0]+new_tar.bbox[2])//2

        dist_sqrt = math.pow(cur_y-last_y,2)+math.pow(cur_x-last_x,2)
        return dist_sqrt

    def check(self,tar): #void
        #exist target
        closest_tar=-1
        closest_distsq=float("inf") #init to max
        for index,exist_tar in enumerate(self.target_list):#compare w each exist tar
            distsq = self.cal_dist(tar,exist_tar)
            if(distsq<closest_distsq): #update closest
                closest_tar=index
                closest_distsq=distsq
        if(closest_distsq<=config.PERMITTED_RANGE_SQRT):
            self.target_list[closest_tar].bbox=tar.bbox
            self.target_list[closest_tar].confidence=tar.confidence
        #new target    
        else:
            self.add(tar)

    def tracking(self,detections): #target[]
        for d in detections:
            self.check(d)
        return self.target_list
#-----------------------------------#