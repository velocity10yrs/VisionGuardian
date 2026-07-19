Camera
   │
   ▼
Detector
   │
   ▼
Event Engine
   │
   ▼
Action Dispatcher
   │
   ├── Screenshot
   ├── Logger
   └── (Future) HTTP API

detector.py: Detect objects from frames.
events.py: Convert detections into business events.
actions.py: Execute actions triggered by events.
logger.py: Record runtime events.
config.py: Centralized configuration management.
