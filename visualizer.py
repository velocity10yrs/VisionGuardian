"""
负责可视化frame中的检测标识
"""
#-----------------------------------# 
import cv2
import config
#-----------------------------------# 
#roi=config.ROI
#-----------------------------------# 
class Visualizer:
    def __init__(self):
        return
    def visualize_tar(self,frame,targets):
        #draw target
        for target in targets:
            if target.state == "EXPIRED":
                continue
            x1,y1,x2,y2=target.bbox
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            info = 'state:'+target.state   #str(target.target_id)+
            cv2.putText(frame,info,(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
        return
    def visualize_roi(self,frame,roi):
        #draw ROI
        rx1,ry1,rx2,ry2=roi
        cv2.rectangle(frame,                     
             (rx1,ry1),
             (rx2,ry2),
             (0,0,255),
             2)
        cv2.putText(frame,"ROI",(rx1,ry1-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
        return