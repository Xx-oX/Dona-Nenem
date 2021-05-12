# NCKU ARXML DOCUMENTATION (?

## Description
* a specificated arxml definition for AUTOSAR OS implementation

## Definition & Hierarchy

### Symbols
MODULE -> OS | Task | Event | Counter | Alarm | ScheduleTable
MODULE_UPPER -> OS | TASK | EVENT | COUNTER | ALARM | SCHEDULETABLE
String -> (a-z | A-Z)(0-9 | a-z | A-Z)*
Boolean -> "TRUE" | "FALSE"
Integer -> (0-9)+

### Top Module
* "<"AR-PACKAGES">": root, same as normal arxml
    * "<"AR-PACKAGE">"
      * "<"SHORT-NAME">": name of module -> (MODULE)"configures"
      * "<"ELEMENTS">": module configuration
        * "<"(MODULE_UPPER)">": see 'Modules'

### Modules
* "<"OS">"
  * "<"SHORT-NAME">": name of OS -> String
  * "<"STATUS">": enum -> "STANDARD" | "EXTENDED"
  * "<"ERRORHOOK">" -> Boolean
  * "<"PRETASKHOOK">" -> Boolaen
  * "<"POSTTASKHOOK">" -> Boolaen
  * "<"STARTUPHOOK">" -> Boolaen
  * "<"SHUTDOWNHOOK">" -> Boolaen
  * "<"USERESSCHEDULER">" -> Boolaen
* "<"APPMODE">": under OSConfigures -> String

* "<"TASK">"
  * "<"SHORT-NAME">": name of Task -> String
  * "<"PRIORITY">": uint32 -> Integer
  * "<"ACTIVATION">": uint32(0~255) -> Integer
  * "<"STACK">": uint16 -> Integer
  * "<"TYPE">": enum -> "BASE" | "EXTENDED"
  * "<"SCHEDULE">": enum -> "NON" | "FULL"
  * "<"RESOURCE">"
    * "<"SHORT-NAME">": name of resource -> String
  * "<"EVENT">"
    * "<"SHORT-NAME">": name of event -> String
  * "<"AUTOSTART">"
    * "<"VALUE">" -> Boolaen
    * "<"APPMODE">": if value = "TRUE" -> String

* "<"EVENT">"
  * "<"SHORT-NAME">": name of Event -> String
  * "<"MASK">": uint64 -> "0x"Integer | "AUTO"

* "<"COUNTER">"
  * "<"SHORT-NAME">": name of Counter -> String
  * "<"MINCYCLE">": uint32 -> Integer
  * "<"MAXALLOWEDVALUE">": uint32 -> Integer
  * "<"TICKSPERBASE">": uint32 -> Integer
  * "<"TYPE">": enum -> "SOFTWARE" | "HARDWARE"

* "<"ALARM">"
  * "<"SHORT-NAME">": name of Alarm -> String
  * "<"COUNTER">"
    * "<"SHORT-NAME">" -> String
  * "<"ACTION">"
    * "<"TYPE">": enum -> "ACTIVATETASK" | "SETEVENT" | "ALARMCALLBACK" | "EPCALLBACK"
    * "<"TASK">": if type = "ACTIVATETASK" or "SETEVENT"
      * "<"SHORT-NAME">" -> String
    * "<"EVENT">": if type = "SETEVENT"
      * "<"SHORT-NAME">" -> String
    * "<"ALARMCALLBACKNAME">": if type = "ALARMCALLBACK" or "EPCALLBACK" -> String
    * "<"AUTOSTART">"
      * "<"VALUE">" -> Boolaen
      * "<"APPMODE">": if value = "TRUE" -> String

* "<"SCHEDULETABLE">"
  * "<"SHORT-NAME">": name of ScheduleTable -> String
  * "<"DURATION">": uint32 -> Integer
  * "<"INITOFFSET">": uint32 -> Integer
  * "<"FINALDELAY">": uint32 -> Integer
  * "<"SYNCSTRATEGY">": enum -> "NONE" | "IMPLICIT" | "EXPLICIT"
  * "<"REPEATING">" -> Boolean
  * "<"COUNTER">"
    * "<"SHORT-NAME">" -> String
  * "<"SYNCCOUNTER">": if syncstrategy = "EXPLICIT"
    * "<"SHORT-NAME">" -> String
 * "<"EXPLICITPRECISION">": if syncstrategy = "EXPLICIT", uint32 -> Integer
  * "<"CALLBACKALARM">" -> String
  * "<"AUTOSTART">"
    * "<"VALUE">" -> Boolaen
    * "<"TYPE">" -> enum -> "RELATIVE" | "ABSOLUTE" | "SYNCHRON"
    * "<"APPMODE">": if value = "TRUE" -> String
  * "<"EXPIRYPOINTS">"
    * "<"ELEMENTS">": set of ExpiryPoints, defined below

*submodule*
* "<"EXPIRYPOINT">"
  * "<"SHORT-NAME">": name of ExpiryPoint
  * "<"OFFSET">": uint32 -> Integer
  * "<"MAXSHORTEN">": uint32 -> Integer
  * "<"MAXLENGTHEN">": uint32 -> Integer
  * "<"TASKACTIVATION">"
    * "<"ELEMENTS">": set of Tasks
      * "<"TASK">"
        * "<"SHORT-NAME">" -> String
        ...
  * "<"EVENTSETTINGS">"
    * "<"ELEMENTS">": set of EventSettings
      * "<"EVENTSETTING">"
        * "<"SHORT-NAME">" -> String
        * "<"TASK">"
          * "<"SHORT-NAME">" -> String
        * "<"EVENT">"
          * "<"SHORT-NAME">" -> String
      ...

### Not support yet
* "<"RESOURCE">"
  * "<"SHORT-NAME">": name of Resource
  * "<"RESOURCEPROPERTY">": enum -> "STANDARD" | "INTERNAL"

* "<"ISR">"
  * "<"SHORT-NAME">": name of ISR
  * "<"CATEGORY">": uint32 -> Integer
  * "<"RESOURCE">"
    * "<"SHORT-NAME">" -> String
  * "<"INTERRUPT">": enum -> ({0~281} - {26, 34, 76})
  * "<"STACK">": uint16 -> Integer
  * "<"PRIORITY">": uint32 -> Integer

## Example
```
<?xml version="1.0" encoding="utf-8"?>
<AR-PACKAGES>
    <AR-PACKAGE>
        <SHORT-NAME>OSConfigures</SHORT-NAME>
        <ELEMENTS>
            <OS>
                <SHORT-NAME>ExampleOS</SHORT-NAME>
                <STATUS>EXTENDED</STATUS>
                <ERRORHOOK>TRUE</ERRORHOOK>
                <PRETASKHOOK>FALSE</PRETASKHOOK>
                <POSTTASKHOOK>FALSE</POSTTASKHOOK>
                <STARTUPHOOK>FALSE</STARTUPHOOK>
                <SHUTDOWNHOOK>FALSE</SHUTDOWNHOOK>
                <USERESSCHEDULER>FALSE</USERESSCHEDULER>
            </OS>
            <APPMODE>AppMode1</APPMODE>
        </ELEMENTS>
    </AR-PACKAGE>
    <AR-PACKAGE>
        <SHORT-NAME>TaskConfigures</SHORT-NAME>
        <ELEMENTS>
            <TASK>
                <SHORT-NAME>TaskStart</SHORT-NAME>
                <PRIORITY>1</PRIORITY>
                <ACTIVATION>1</ACTIVATION>
                <STACK>512</STACK>
                <TYPE>BASIC</TYPE>
                <SCHEDULE>FULL</SCHEDULE>
                <AUTOSTART>
                    <VALUE>TRUE</VALUE>
                    <APPMODE>AppMode1</APPMODE>
                </AUTOSTART>
            </TASK>
            <TASK>
                <SHORT-NAME>TaskA</SHORT-NAME>
                <PRIORITY>1</PRIORITY>
                <ACTIVATION>1</ACTIVATION>
                <STACK>512</STACK>
                <TYPE>BASIC</TYPE>
                <SCHEDULE>FULL</SCHEDULE>
                <AUTOSTART>
                    <VALUE>FALSE</VALUE>
                </AUTOSTART>
            </TASK>
            <TASK>
                <SHORT-NAME>TaskB</SHORT-NAME>
                <PRIORITY>2</PRIORITY>
                <ACTIVATION>1</ACTIVATION>
                <STACK>512</STACK>
                <TYPE>BASIC</TYPE>
                <SCHEDULE>FULL</SCHEDULE>
                <AUTOSTART>
                    <VALUE>FALSE</VALUE>
                </AUTOSTART>
            </TASK>
            <TASK>
                <SHORT-NAME>TaskC</SHORT-NAME>
                <PRIORITY>2</PRIORITY>
                <ACTIVATION>10</ACTIVATION>
                <STACK>512</STACK>
                <TYPE>BASIC</TYPE>
                <SCHEDULE>FULL</SCHEDULE>
                <AUTOSTART>
                    <VALUE>FALSE</VALUE>
                </AUTOSTART>
            </TASK>
            <TASK>
                <SHORT-NAME>TaskD</SHORT-NAME>
                <PRIORITY>1</PRIORITY>
                <ACTIVATION>10</ACTIVATION>
                <STACK>512</STACK>
                <TYPE>EXTENDED</TYPE>
                <SCHEDULE>FULL</SCHEDULE>
                <AUTOSTART>
                    <VALUE>FALSE</VALUE>
                </AUTOSTART>
                <EVENT>EventP</EVENT>
            </TASK>
        </ELEMENTS>
    </AR-PACKAGE>
    <AR-PACKAGE>
        <SHORT-NAME>EventConfigures</SHORT-NAME>
        <ELEMENTS>
            <EVENT>
                <SHORT-NAME>EventP</SHORT-NAME>
                <MASK>AUTO</MASK>
            </EVENT>
        </ELEMENTS>
    </AR-PACKAGE>
    <AR-PACKAGE>
        <SHORT-NAME>CounterConfigures</SHORT-NAME>
        <ELEMENTS>
            <COUNTER>
                <SHORT-NAME>CounterA</SHORT-NAME>
                <MINCYCLE>10</MINCYCLE>
                <MAXALLOWEDVALUE>20</MAXALLOWEDVALUE>
                <TICKSPERBASE>10</TICKSPERBASE>
                <TYPE>SOFTWARE</TYPE>
            </COUNTER>
        </ELEMENTS>
    </AR-PACKAGE>
    <AR-PACKAGE>
        <SHORT-NAME>AlarmConfigures</SHORT-NAME>
        <ELEMENTS>
            <ALARM>
                <SHORT-NAME>epAlarmA</SHORT-NAME>
                <COUNTER>
                    <SHORT-NAME>CounterA</SHORT-NAME>
                </COUNTER>
                <ACTION>
                    <TYPE>EPCALLBACK</TYPE>
                    <ALARMCALLBACKNAME>ExpiryPointCallbackFuncA</ALARMCALLBACKNAME>
                </ACTION>
                <AUTOSTART>
                    <VALUE>FALSE</VALUE>
                </AUTOSTART>
            </ALARM>
        </ELEMENTS>
    </AR-PACKAGE>
    <AR-PACKAGE>
        <SHORT-NAME>ScheduleTableConfigures</SHORT-NAME>
        <ELEMENTS>
            <SCHEDULETABLE>
                <SHORT-NAME>ScheduleTableA</SHORT-NAME>
                <DURATION>10</DURATION>
                <INITOFFSET>2</INITOFFSET>
                <FINALDELAY>6</FINALDELAY>
                <SYNCSTRATEGY>NONE</SYNCSTRATEGY>
                <REPEATING>TRUE</REPEATING>
                <COUNTER>
                    <SHORT-NAME>CounterA</SHORT-NAME>
                </COUNTER>
                <CALLBACKALARM>epAlarmA</CALLBACKALARM>
                <EXPIRYPOINTS>
                    <ELEMENTS>
                        <EXPIRYPOINT>
                            <SHORT-NAME>EP1</SHORT-NAME>
                            <OFFSET>2</OFFSET>
                            <MAXSHORTEN>0</MAXSHORTEN>
                            <MAXLENGTHEN>0</MAXLENGTHEN>
                            <TASKACTIVATION>
                                <ELEMENTS>
                                    <TASK>
                                        <SHORT-NAME>TaskA</SHORT-NAME>
                                    </TASK>
                                    <TASK>
                                        <SHORT-NAME>TaskB</SHORT-NAME>
                                    </TASK>
                                </ELEMENTS>
                            </TASKACTIVATION>
                        </EXPIRYPOINT>
                        <EXPIRYPOINT>
                            <SHORT-NAME>EP2</SHORT-NAME>
                            <OFFSET>4</OFFSET>
                            <MAXSHORTEN>0</MAXSHORTEN>
                            <MAXLENGTHEN>0</MAXLENGTHEN>
                            <TASKACTIVATIONS>
                                <ELEMENTS>
                                    <TASK>
                                        <SHORT-NAME>TaskC</SHORT-NAME>
                                    </TASK>
                                </ELEMENTS>
                            </TASKACTIVATIONS>
                            <EVENTSETTINGS>
                                <ELEMENTS>
                                    <EVENTSETTING>
                                        <SHORT-NAME>E1</SHORT-NAME>
                                        <TASK>
                                            <SHORT-NAME>TaskD</SHORT-NAME>
                                        </TASK>
                                        <EVENT>
                                            <SHORT-NAME>EventP</SHORT-NAME>
                                        </EVENT>
                                    </EVENTSETTING>
                                </ELEMENTS>
                            </EVENTSETTINGS>
                        </EXPIRYPOINT>
                    </ELEMENTS>
                </EXPIRYPOINTS>
                <AUTOSTART>
                    <VALUE>TRUE</VALUE>
                    <TYPE>RELATIVE</TYPE>
                    <APPMODE>AppMode1</APPMODE>
                </AUTOSTART>
            </SCHEDULETABLE>
        </ELEMENTS>
    </AR-PACKAGE>
</AR-PACKAGES>
```
