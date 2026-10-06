VisionGuardian

AI Event-driven Video Monitoring System

VisionGuardian is a modular, local-first video monitoring system built with Python, OpenCV and YOLO.

Documentation: [系统规格书 / 功能规格书](docs/specification.md)

v0.1 focuses on establishing the fundamental pipeline from camera input to AI detection, event generation and automated response.

Overview

VisionGuardian is an experimental Edge AI video monitoring project designed to explore how computer vision can be transformed from frame-level detection into an event-driven monitoring system.

The project separates:

Detection — what the camera/AI model observes
State — the current condition of the monitored target
Event — what the system determines has happened
Action — what the system does in response

The initial use case is detecting a person entering a defined Region of Interest (ROI).

All processing and event data are handled locally.

v0.1.0 Scope

The first version intentionally focuses on a minimal single-camera, single-target monitoring scenario.

Supported
Real-time USB camera input
OpenCV frame processing
YOLO-based person detection
Rectangular ROI monitoring
Intrusion event generation
Basic event state management
Warning generation
Screenshot capture
Event logging
Graceful camera/window cleanup
Current limitations

v0.1 is a baseline implementation rather than a production-ready monitoring system.

It currently assumes:

Single target
Single camera
Frame-by-frame detection
Simple ROI logic
No persistent target identity
No temporal tracking

In complex environments, YOLO detection may fluctuate between frames. Such fluctuations can cause a target near an ROI boundary to temporarily disappear from the detection results and subsequently generate another event.

These issues are intentionally left for later versions.

Architecture
                    VisionGuardian v0.1

┌──────────┐
│  Camera  │
└────┬─────┘
     │ Frame
     ▼
┌──────────────┐
│   Detector   │
│ YOLO / OpenCV│
└────┬─────────┘
     │ Detection[]
     ▼
┌────────────────┐
│  EventEngine   │
│ ROI + State    │
└────┬───────────┘
     │ Event[]
     ▼
┌────────────────┐
│ ActionHandler  │
├────────────────┤
│ Warning        │
│ Screenshot     │
│ Logging        │
└────────────────┘
Component responsibilities
Camera / Pipeline

Responsible for:

acquiring frames
controlling the processing loop
passing data between components
handling shutdown and resource cleanup

The pipeline itself does not contain business rules.

Detector

Responsible for:

What did the AI model observe?

The detector receives a frame and returns lightweight detection information:

confidence
bounding box

YOLO model inference is encapsulated inside this component.

EventEngine

Responsible for:

Does the current observation constitute a meaningful event?

The v0.1 implementation:

evaluates whether a target is inside the ROI
maintains a simple intrusion state
generates an intrusion Event only when the target transitions into the ROI

This separates raw AI observations from application-level events.

Event

An Event represents a structured record of something the system has determined to have happened.

Current Event information includes:

event_type
confidence
bbox
timestamp

Example:

Event(
    event_type="intrusion",
    confidence=0.91,
    bbox=(...),
    timestamp=...
)
ActionHandler

Responsible for responding to events.

For intrusion, v0.1 performs:

intrusion
   ├── Warning
   ├── Screenshot
   └── Log
Data Flow

A single frame is processed through the system as follows:

Frame
  │
  ▼
Detector
  │
  └── Detection[]
          │
          ▼
     EventEngine
          │
          └── Event[]
                  │
                  ▼
             ActionHandler

The overall process repeats continuously:

Frame 1 → Detection → Event → Action
Frame 2 → Detection → Event → Action
Frame 3 → Detection → Event → Action
...

Detection[] and Event[] are ordinary Python lists representing the results associated with the current frame. The continuous stream is provided by the camera processing loop rather than by the lists themselves.

Event Model

The v0.1 event model uses a simple state transition:

OUTSIDE
   │
   │ target enters ROI
   ▼
INTRUDED
   │
   │ target remains inside
   │
   └───────────────┐
                   │
                   ▼
              no new event

INTRUDED
   │
   │ target leaves ROI
   ▼
OUTSIDE

When the target enters the ROI for the first time, an intrusion Event is generated.

Continuous detection while the target remains inside the ROI does not repeatedly generate the same event.

Project Structure
VisionGuardian/
│
├── main.py
├── detector.py
├── events.py
├── actions.py
├── config.py
├── logger.py
├── requirements.txt
├── README.md
│
├── logs/
│   └── .gitkeep
│
├── screenshots/
│   └── .gitkeep
│
└── models/
    └── ...

Generated runtime data such as screenshots and logs should normally remain outside version control unless they are intentionally included as demonstration artifacts.

Technology Stack
Component	Technology
Language	Python 3.x
Computer Vision	OpenCV
Numerical Processing	NumPy
Object Detection	Ultralytics YOLO
Input	USB Camera
Storage	Local files
Development	VS Code
Running

Install dependencies:

pip install -r requirements.txt

Then start the monitoring pipeline:

python main.py

A connected camera is required.

Press:

q

to terminate the monitoring window.

When the application exits, the pipeline releases the camera and closes OpenCV windows.

Output

When an intrusion event is generated, the system produces three forms of response.

Console
Warning: [HH:MM:SS] person intruded ROI.
Screenshot
screenshots/
└── intrusion_YYYYMMDD_HHMMSS.jpg
Log
logs/
└── ...

The log records the warning and the corresponding screenshot.

Design Philosophy

VisionGuardian is intentionally designed around an event-driven architecture.

The central distinction is:

Detection
    ↓
"What did we observe?"

EventEngine
    ↓
"What does this observation mean?"

Event
    ↓
"What happened?"

Action
    ↓
"What should the system do?"

This separation allows the detection mechanism and response mechanisms to evolve independently.

For example, future versions may replace or extend the YOLO detector without requiring the warning, logging or screenshot components to understand how object detection works.

Known Limitations
Detection jitter

YOLO performs frame-level detection. Even when a person is stationary, bounding boxes and confidence values may fluctuate slightly between frames.

Near an ROI boundary, this may cause:

INSIDE
OUTSIDE
INSIDE
OUTSIDE

and consequently multiple intrusion events.

Multiple targets

The v0.1 state machine maintains a single intrusion state:

self.is_intruded

Therefore, multiple simultaneous targets are outside the intended scope of this version.

No tracking

The system does not currently maintain persistent target identities between frames.

No temporal filtering

There is currently no:

hysteresis
cooldown
temporal smoothing
frame skipping
lost-target timeout

These are planned for later versions.
