import time 

def append_log(level,module,event,message):

    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    #ver(2026-0806 19:50)
        #print("timestamp:",current_time)
        #print("level:",level)
        #print("module:",module)
        #print("Event:",event)
        #print("Message:",message)

    #ver(2026-0806 20:01)
    print("timestamp:",current_time,"\n",
          "level:",level,"\n",
          "module:",module,"\n",
          "Event:",event,"\n",
          "Message:",message)

    return