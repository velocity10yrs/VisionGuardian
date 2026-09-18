import cv2
from detector import Detector
from events import EventEngine
from actions import ActionHandler
from tracker import Tracker

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
        detector = Detector() 
        tracker = Tracker()
        event_engine = EventEngine() 
        action_handler = ActionHandler() 

        while True:
            ret,frame = camera.read()
            if not ret:
                print("camera data reading failed.")
                return

            #step-2: detecting
            detections = detector.detect(frame) #detect()

            #step-new: target tracing
            targets = tracker.tracking(detections) #track()

            #step-3: event triggered
            events = event_engine.verify(targets)#event_engine

            #step-4: taking action
            action_handler.handle_event(events) #action_handler

            #step-5: quit camera
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

    
#start the system:
if __name__ == "__main__":
    main()
