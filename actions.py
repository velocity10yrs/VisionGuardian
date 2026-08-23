from datetime import datetime

class ActionHandler:

    def handle_event(self,events,frame):
        for e in events: # events=[] f
            if e.event_type == "intrusion":
                self.handle_intrusion(e,frame)

    def warning(self):#解耦
        print(
            f"[{datetime.now():%H:%M:%S}]"
            f"Warning: person intruded ROI."
        ) 

    def logging(self,event):
        return 
    
    def screenshot(self,event,frame):
        return

    def handle_intrusion(self,event,frame):
        self.warning(event)
        self.logging(event)
        self.screenshot(event,frame)

