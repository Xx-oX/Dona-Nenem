import xml.etree.ElementTree as ET

def parse(file):
    print("Parsing...")
    tree = ET.parse(file)
    root = tree.getroot()
    AST = list()
    try:
        for arpackage in root.findall("AR-PACKAGE"):
            for elements in arpackage.findall("ELEMENTS"):
                for element in elements:
                    AST.append(element)
    except:
        print("Parsing Error!!!")

    print("Complete!!!")
    return AST

def gen(AST, file):
    print("Generating OIL Code...")
    taskList = list()
    eventList = list()
    counterList = list()
    alarmList = list()
    scheduleTableList = list()
    appMode = ""

    # get configure infomations
    for element in AST:
        if element.tag == "OS":
            osCfg = element
        elif element.tag == "APPMODE":
            appMode = element.text
        elif element.tag == "TASK":
            taskList.append(element)
        elif element.tag == "EVENT":
            eventList.append(element)
        elif element.tag == "COUNTER":
            counterList.append(element)
        elif element.tag == "ALARM":
            alarmList.append(element)
        elif element.tag == "SCHEDULETABLE":
            scheduleTableList.append(element)

    #try:
        fp = open(file, "w")

        # begin OSEK
        fp.write("OSEK OSEK {\n\n")

        # begin OSCFG
        fp.write("    OS " + osCfg.find("SHORT-NAME").text + " {\n")
        fp.write("        STATUS = " + osCfg.find("STATUS").text + ";\n")
        fp.write("        ERRORHOOK = " + osCfg.find("ERRORHOOK").text + ";\n")
        fp.write("        PRETASKHOOK = " + osCfg.find("PRETASKHOOK").text + ";\n")
        fp.write("        POSTTASKHOOK = " + osCfg.find("POSTTASKHOOK").text + ";\n")
        fp.write("        STARTUPHOOK = " + osCfg.find("STARTUPHOOK").text + ";\n")
        fp.write("        SHUTDOWNHOOK = " + osCfg.find("SHUTDOWNHOOK").text + ";\n")
        fp.write("        USERESSCHEDULER = " + osCfg.find("USERESSCHEDULER").text + ";\n")
        fp.write("    };\n\n")
        #end OSCFG
        
        # begin APPMODE
        fp.write("    APPMODE = " + appMode + ";\n\n")
        # end APPMODE 

        # begin TASKCFFG
        for task in taskList:
            fp.write("    TASK " + task.find("SHORT-NAME").text + " {\n")
            fp.write("        PRIORITY = " + task.find("PRIORITY").text + ";\n")
            fp.write("        ACTIVATION = " + task.find("ACTIVATION").text + ";\n")
            fp.write("        STACK = " + task.find("STACK").text + ";\n")
            fp.write("        TYPE = " + task.find("TYPE").text + ";\n")
            fp.write("        SCHEDULE = " + task.find("SCHEDULE").text + ";\n")
            fp.write("        AUTOSTART = " + task.find("AUTOSTART").find("VALUE").text)

            if task.find("AUTOSTART").find("VALUE").text == "TRUE":
                fp.write(" {\n")
                fp.write("            APPMODE = " + task.find("AUTOSTART").find("APPMODE").text + ";\n")
                fp.write("        }\n")
            else:
                fp.write(";\n")            
            
            fp.write("    };\n\n")
        # end TASKCFG

        # begin EVENTCFG
        for event in eventList:
            fp.write("    EVENT " + event.find("SHORT-NAME").text + " {\n")
            fp.write("        MASK = "+ event.find("MASK").text + ";\n")
            fp.write("    };\n\n")
        # end EVENTCFG

        # begin COUNTERCFG
        for counter in counterList:
            fp.write("    COUNTER " + counter.find("SHORT-NAME").text + " {\n")
            fp.write("        MINCYCLE = " + counter.find("MINCYCLE").text + ";\n")
            fp.write("        MAXALLOWEDVALUE = " + counter.find("MAXALLOWEDVALUE").text + ";\n")
            fp.write("        TICKSPERBASE = " + counter.find("TICKSPERBASE").text + ";\n")
            fp.write("        COUNTERTYPE = " + counter.find("TYPE").text + ";\n")
            fp.write("    };\n\n")
        # end COUNTERCFG

        # begin ALARMCFG
        for alarm in alarmList:
            fp.write("    ALARM " + alarm.find("SHORT-NAME").text + " {\n")
            fp.write("        COUNTER = " + alarm.find("COUNTER").find("SHORT-NAME").text + ";\n")
            
            fp.write("        ACTION = " + alarm.find("ACTION").find("TYPE").text + " {\n")
            alarmAction = alarm.find("ACTION")
            if alarmAction.find("TYPE").text == "ACTIVATETASK":
                fp.write("            TASK = " + alarmAction.find("TASK").find("SHORT-NAME").text + ";\n")
            elif alarmAction.find("TYPE").text == "SETEVENT":
                fp.write("            TASK = " + alarmAction.find("TASK").find("SHORT-NAME").text + ";\n")
                fp.write("            EVENT = " + alarmAction.find("EVENT").find("SHORT-NAME").text + ";\n")
            elif alarmAction.find("TYPE").text == "ALARMCALLBACK" or alarmAction.find("TYPE").text == "EPCALLBACK":
                fp.write("            ALARMCALLBACKNAME = \"" + alarmAction.find("ALARMCALLBACKNAME").text + "\";\n")
            fp.write("        };\n")

            fp.write("        AUTOSTART =" + alarm.find("AUTOSTART").find("VALUE").text)
            if alarm.find("AUTOSTART").find("VALUE").text == "TRUE":
                fp.write(" {\n")
                fp.write("            ALARMTIME = " + alarm.find("AUTOSTART").find("ALARMTIME").text + ";\n")
                fp.write("            ALARMTIME = " + alarm.find("AUTOSTART").find("CYCLETIME").text + ";\n")
                fp.write("            ALARMTIME = " + alarm.find("AUTOSTART").find("APPMODE").text + ";\n")
                fp.write("        }\n")
            else:
                fp.write(";\n")    

            fp.write("    };\n\n")
        # end ALARMCFG

        # end OSEK
        fp.write("\n};\n")

        fp.close()
    #except AttributeError:
    #s    print("Tag Error!!!")
    #except:
    #    print("Code Gen Error!!!")

    print("Complete!!!")
