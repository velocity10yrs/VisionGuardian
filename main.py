import cv2
from detector import Detector
from logger import append_log
from actions import save_screenshot

def main():
    print("starting the system:")
    run_pipeline()
    
def run_pipeline():
    #step-1: cam process
    camera=cv2.VideoCapture(0)
    is_cam_on,frame = camera.read()
    if not is_cam_on:
        print("cam initialization failed")
        return
    print("cam is on.")

    #step-2: detecting
    detector = Detector()
    detections = detector.detect(frame)

    #step-3: event triggered
    event_engine=EventEngine() #stub
    events = event_engine.detect(detections)#event_engine还没定义,但先写接口再实现

    #step-4: taking action
    actions=ActionHandler() #stub
    actions.handle_event(events) #actions.execute()同理

#以下是构建pipeline时尚未搭建的stub:
class EventEngine:
    def detect(self,detections):
        return []
class ActionHandler:
    def handle_event(self,events):
        return 
    
#start the system:
if __name__ == "__main__":
    main()
