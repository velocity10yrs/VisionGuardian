import cv2
from detector import Detector
from logger import append_log
from actions import save_screenshot

def main():
    print("starting the system:")
    run_pipeline()
    
def run_pipeline():
    camera = None 
    #step-1: try turn on the camera 
    try:
        camera = cv2.VideoCapture(0)  
        if not camera.isOpened():
            print("cam initialization failed..")
            return
        print("cam is on.")
        #step-1.1: components initializing
        detector = Detector() #stub
        event_engine = EventEngine() #stub
        action_handler = ActionHandler() #stub

        while True:
            ret,frame = camera.read()
            if not ret:
                print("camera data reading failed.")
                return
            #print("camera data flow incoming...")#fixed:刷屏

            #step-2: detecting
            detections = detector.detect(frame) #detect()待实现

            #step-3: event triggered
            events = event_engine.detect(detections)#event_engine待实现

            #step-4: taking action
            action_handler.handle_event(events) #action_handler待实现

            #step-5: quit camera
            #print("press 'q' to quit at anytime")#fixed:刷屏
            cv2.imshow("camera_1",frame)
            if(cv2.waitKey(1)&0xff==ord('q')):
                print("quit camera_1.")
                return
    finally:
        #step-6: clean up
        print("pipeline cleanup started,")
        if camera is not None:
            camera.release()
        print("cam released,")
        cv2.destroyAllWindows()
        print("all windows are closed.")

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
