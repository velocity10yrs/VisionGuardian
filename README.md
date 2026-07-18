/***2026-07-15 10:29***/  文件目录
    PROJECT <Vision Guardian>(ver 0.1) Created:
    VisionGuard/
    │
    ├── main.py     #入口
    ├── detector.py #输入frame,输出result
    ├── events.py   #筛选目标,设定ROI,生成event
    ├── actions.py  #收到event,执行action
    ├── logger.py   #追加日志
    ├── config.py   #常量设定集中处
    │
    ├── screenshots/
    ├── logs/
    │
    ├── requirements.txt
    ├── README.md
    └── .gitignore
/****2026-07-18 15:59****/ 系统架构图
Camera
   │
   ▼
Detector
   │
   ▼
Event Engine
   │
   ▼
Actions
   │
   ├── Screenshot
   └── Logger
   └── (Future) HTTP API
   │
   ▼
Display
2026-07-16 10:23 配置了config.py, events.py, actions.py, detector.py, logger.py;
2026-07-18 07:23 细化了config.py;
           16:03 README.md, 编写了main.py主流程; 