from detector import Detector

from logger import append_log

from actions import save_screenshot

def main():

    frame = camare.read()

    detections = detector.detect(frame)
    
    events = event_engine.detect(detections)
    
    actions.execute(events)