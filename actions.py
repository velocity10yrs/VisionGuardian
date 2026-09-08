import cv2
import os
from datetime import datetime
import config

class ActionHandler:

    def get_timestamp(self):
        timestamp = datetime.now()
        return timestamp
    
    def generate_warning(self):#解耦
        now = self.get_timestamp()
        warning=f"Warning: [{now:%H:%M:%S}] person intruded ROI."
        print(warning)
        return warning

    def append_log(self,event,warning,ssname):
        with open(config.LOG_DIR+config.LOG_FILE,'a',encoding="utf-8") as f:
            f.write(warning+'\n')
            f.write("screenshot saved as: "+ssname+'\n')
            f.write('-'*40+'\n')#隔行记号
    
    def generate_screenshot(self,event,frame):
        now = self.get_timestamp()
        ssname = event.event_type+now.strftime("%Y%m%d_%H%M%S")+".jpg"
        filepath = os.path.join(config.SCREENSHOT_DIR,ssname)
        is_saved = cv2.imwrite(filepath,frame)
        if is_saved:
            return ssname
        else:
            return "screenshot failure"

    def handle_intrusion(self,event,frame):
        warning = self.generate_warning()
        ssname = self.generate_screenshot(event,frame)
        self.append_log(event,warning,ssname)

    def handle_event(self,events,frame):
        for e in events: 
            if e.event_type == "intrusion":
                print("event received")#debug
                self.handle_intrusion(e,frame)
