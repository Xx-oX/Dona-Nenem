#!/usr/bin/env python

import sys
import traceback
import xml.etree.ElementTree as ET

def parse(file):
    AST = list()
    try:
        print("Parsing...")
        tree = ET.parse(file)
        root = tree.getroot()
        for arpackage in root.findall("AR-PACKAGE"):
            for elements in arpackage.findall("ELEMENTS"):
                for element in elements:
                    AST.append(element)
        print("Complete!!!")
    except Exception as e:
        errType = e.__class__.__name__
        errDetail = e.args[0]
        cl, exc, tb = sys.exc_info()
        lastCallStack = traceback.extract_tb(tb)[-1]
        fileName = lastCallStack[0]
        lineNum = lastCallStack[1]
        funcName = lastCallStack[2]
        errMsg = "Parsing Error!!!\nFile \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, errType, errDetail)
        print(errMsg)
        AST = list()
    return AST

def gen(AST, file):
    if not AST:
        return
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

    try:
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

            if task.find("TYPE").text == "EXTENDED":
                taskEventList = list()
                taskResourceList = list()
                if task.find("EVENT"):
                    for element in task.findall("EVENT"):
                        taskEventList.append(element.find("SHORT-NAME").text)
                    fp.write("        EVENT = ")
                    for e in taskEventList:
                        fp.write(e)
                        if e == taskEventList[-1]:
                            fp.write(";\n")
                        else:
                            fp.write(" | ")

                if task.find("RESOURCE"):
                    for element in task.findall("RESOURCE"):
                        taskResourceList.append(element.find("SHORT-NAME").text)
                    for e in taskResourceList:
                        fp.write("        RESOURCE = " + e + ";\n")



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
                fp.write("            CYCLETIME = " + alarm.find("AUTOSTART").find("CYCLETIME").text + ";\n")
                fp.write("            APPMODE = " + alarm.find("AUTOSTART").find("APPMODE").text + ";\n")
                fp.write("        }\n")
            else:
                fp.write(";\n")

            fp.write("    };\n\n")
        # end ALARMCFG

        # begin SCHEDULETABLECFG
        for st in scheduleTableList:
            fp.write("    SCHEDULETABLE " + st.find("SHORT-NAME").text + "{\n")
            fp.write("        DURATION = " + st.find("DURATION").text + ";\n")
            fp.write("        INITOFFSET = " + st.find("INITOFFSET").text + ";\n")
            fp.write("        FINALDELAY = " + st.find("FINALDELAY").text + ";\n")
            fp.write("        SYNCSTRATEGY = " + st.find("SYNCSTRATEGY").text + ";\n")
            fp.write("        REPEATING = " + st.find("REPEATING").text + ";\n")
            fp.write("        COUNTER = " + st.find("COUNTER").find("SHORT-NAME").text + ";\n")
            fp.write("        CALLBACKALARM = " + st.find("CALLBACKALARM").text + ";\n")

            if st.find("SYNCSTRATEGY").text == "EXPLICIT":
                fp.write("        SYNCCOUNTER = " + st.find("SYNCCOUNTER").find("SHORT-NAME").text + ";\n")
                fp.write("        EXPLICITPRECISION = " + st.find("EXPLICITPRECISION").text + ";\n")

            expiryPointList = list()
            expiryPointList = st.find("EXPIRYPOINTS").find("ELEMENTS").findall("EXPIRYPOINT")

            for ep in expiryPointList:
                fp.write("        EXPIRYPOINT " + ep.find("SHORT-NAME").text + " {\n")
                fp.write("            OFFSET = " + ep.find("OFFSET").text + ";\n")
                fp.write("            MAXSHORTEN = " + ep.find("MAXSHORTEN").text + ";\n")
                fp.write("            MAXLENGTHEN = " + ep.find("MAXLENGTHEN").text + ";\n")

                epTaskList = list()
                epEventList = list()

                if ep.find("TASKACTIVATION"):
                    for t in ep.find("TASKACTIVATION").find("ELEMENTS").findall("TASK"):
                        epTaskList.append(t)

                if ep.find("EVENTSETTINGS"):
                    for e in ep.find("EVENTSETTINGS").find("ELEMENTS").findall("EVENTSETTING"):
                        epEventList.append(e)

                if not epTaskList and not epEventList:
                    print("Semantic Error -> Taskactivation and eventsetting in a expiry point can't be both empty.")
                    return

                if epTaskList:
                    fp.write("            TASKACTIVATION = ")
                    for t in epTaskList:
                        fp.write(t.find("SHORT-NAME").text)
                        if t == epTaskList[-1]:
                            fp.write(";\n")
                        else:
                            fp.write(", ")

                for e in epEventList:
                    fp.write("            EVENTSETTING " + e.find("SHORT-NAME").text + " {\n")
                    fp.write("                TASK = " + e.find("TASK").find("SHORT-NAME").text + ";\n")
                    fp.write("                EVENT = " + e.find("EVENT").find("SHORT-NAME").text + ";\n")
                    fp.write("            }\n")

                fp.write("        };\n")

            fp.write("        AUTOSTART =" + alarm.find("AUTOSTART").find("VALUE").text)
            if alarm.find("AUTOSTART").find("VALUE").text == "TRUE":
                fp.write(" {\n")
                fp.write("            AUTOSTARTTYPE = " + st.find("AUTOSTART").find("TYPE").text + ";\n")
                fp.write("            APPMODE = " + st.find("AUTOSTART").find("APPMODE").text + ";\n")
                fp.write("        }\n")
            else:
                fp.write(";\n")

            fp.write("    };\n\n")
        # end SCHEDULETABLECFG

        # end OSEK
        fp.write("};\n")

        fp.close()
        print("Complete!!!")

    except Exception as e:
        errType = e.__class__.__name__
        errDetail = e.args[0]
        cl, exc, tb = sys.exc_info()
        lastCallStack = traceback.extract_tb(tb)[-1]
        fileName = lastCallStack[0]
        lineNum = lastCallStack[1]
        funcName = lastCallStack[2]
        errMsg = "Code Gen Error!!!\nFile \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, errType, errDetail)
        print(errMsg)
        open(file, 'w').close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Wrong argument!!!")

    file_in = ""
    file_out = ""

    file_in = sys.argv[1]
    if file_in.count(".arxml") < 1:
        sys.exit("Wrong input file type!!")
    file_out = file_in[:file_in.index(".arxml")] + ".oil"

    AST = parse(file_in)
    gen(AST, file_out)
