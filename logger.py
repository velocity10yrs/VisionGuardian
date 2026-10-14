import time 

def append_log(level,module,event,message):

    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    print("timestamp:",current_time,"\n",
          "level:",level,"\n",
          "module:",module,"\n",
          "Event:",event,"\n",
          "Message:",message)

    return