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
    def __init__(self,target_id=0,bbox=(0,0,0,0),conf=0.0,last_seen=0,state=""):
        self.target_id=target_id
        self.bbox=bbox
        self.confidence=conf
        self.last_seen=last_seen
        self.state=state
#-----------------------------------# 管理者
class Tracker:
    def __init__(self):
        self.current_id=0
        self.target_list=[]

    def add(self,tar):
        self.target_list.append(tar)

    def check(self,tar):
        last_tar = self.target_list[-1]
        last_y = (last_tar.bbox[1]+last_tar.bbox[3])//2
        last_x = (last_tar.bbox[0]+last_tar.bbox[2])//2

        cur_y  = (tar.bbox[1]+tar.bbox[3])//2
        cur_x  = (tar.bbox[0]+tar.bbox[2])//2

        dist_sqrt = math.pow(cur_y-last_y,2)+math.pow(cur_x-last_x,2)
        if(dist_sqrt<=config.PERMITTED_RANGE):
            self.target_list[-1].bbox=tar.bbox
        else:
            self.target_id+=1
            new_target = Target(self.target_id,
                                tar.bbox,
                                tar.conf,
                                last_seen=datetime.now(),
                                state="DETECTED")
            self.add(new_target)
#-----------------------------------#