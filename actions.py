from datetime import datetime

class ActionHandler:

    def handle_event(self,events):
        for e in events: # events=[] f
            if e.event_type == "intrusion":
                self.handle_intrusion()

    def warning(self):#解耦
        print(
            f"[{datetime.now():%H:%M:%S}]"
            f"Warning: person intruded ROI."
        ) 

    def handle_intrusion(self):
        self.warning()

