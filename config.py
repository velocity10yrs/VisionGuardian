
# ======Num_of_camera======
CAMERA_INDEX="0"

#======yolo model======
MODEL_PATH="models/yolo11n.pt"

#======credibility======
CONF_THRESHOLD=0.25

#======ROI======
ROI=(100,100,200,200)
ROI_LINE_X=100
ROI_LINE_Y=100
ENTER_THRESHOLD=0.6
EXIT_THRESHOLD=0.4

#======output======
SCREENSHOT_DIR="screenshots"
LOG_DIR="logs/"
LOG_FILE="event.log"

#======display======
WINDOW_NAME="VisionGuardian"

#======detection======
DETECTION_INTERVAL=3

#======target======
PERMITTED_RANGE=100
TARGET_MISSING_TIMEOUT_SEC=1.0
TARGET_EXPIRE_TIMEOUT_SEC=3.0
JITTER_HISTORY_SIZE=5

#======event======
COOL_DOWN=10