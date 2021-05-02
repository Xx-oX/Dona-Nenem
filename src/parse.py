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

    #get configure infomations
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

        #begin OSEK
        fp.write("OSEK OSEK {\n\n")

        #begin OSCFG
        fp.write("    OS " + osCfg.find("SHORT-NAME").text + " {\n")
        fp.write("        STATUS = " + osCfg.find("STATUS").text + ";\n")
        fp.write("        ERRORHOOK = " + osCfg.find("ERRORHOOK").text + ";\n")
        fp.write("        PRETASKHOOK = " + osCfg.find("PRETASKHOOK").text + ";\n")
        fp.write("        POSTTASKHOOK = " + osCfg.find("POSTTASKHOOK").text + ";\n")
        fp.write("        STARTUPHOOK = " + osCfg.find("STARTUPHOOK").text + ";\n")
        fp.write("        SHUTDOWNHOOK = " + osCfg.find("SHUTDOWNHOOK").text + ";\n")
        fp.write("        USERESSCHEDULER = " + osCfg.find("USERESSCHEDULER").text + ";\n")
        fp.write("    };\n")
        #end OSCFG

        #end OSEK
        fp.write("\n};\n")

        fp.close()
    except:
        print("Code Gen Error!!!")

    print("Complete!!!")
