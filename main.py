import cv2

from detector import Detector

from logger import append_log

from actions import save_screenshot

def main():
    run_pipeline()
    
def run_pipeline():
    camera=cv2.CaptureVideo(0)
    frame = camera.read()

    detector=detector()
    detections = detector.detect(frame)
    
    events = detector.detect(detections)#event_engine还没定义,但先写接口再实现
    
    append_log.handel_events(events) #actions.execute()同理