from functions import *

def checkAddLectureSlot(indexDay: int, hour : int, minute: int, durationMinutes : int, exceptID: int = None):
    query = 'SELECT arrSessions FROM sources '
    if exceptID is not None:
        query += "WHERE ID <> " + str(exceptID)

    cursor.execute(query)
    result = cursor.fetchall()
    condition = True
    for x in result:
        json = ast.literal_eval(x)
        if json[weekdays[indexDay]]['areThereLectures']:
            arrStartTime = json[weekdays[indexDay]]['timeLectures']['timeStartDateLecture'].split(':')
            arrEndTime = json[weekdays[indexDay]]['timeLectures']['timeEndDateLecture'].split(':')
            minuteStart = int(arrStartTime[0])*60 + int(arrStartTime[1])
            minuteEnd = int(arrEndTime[0])*60 + int(arrEndTime[1])
            
            # !!! FIX FIX FIX I have to understand when I can convalidate a slot :D
            condPUSH = True



def getSourceSlots(defaults : dict = None):

    infos = {} 

    rows = []

    defaultStartDate = ""
    defaultEndDate = ""
    
    if defaults != {} and defaults is not None:
        infos = copy.copy(defaults)
        if 'startDateLectures' in defaults and 'endDateLectures' in defaults:
            defaultStartDate = defaults['startDateLectures']
            defaultEndDate = defaults['endDateLectures']
    
    for x in range(7):
        weekday = weekdays[x]

        defaultCheck = False

        defaultStartHour = "09"
        defaultStartMinute = "00"
        defaultEndHour = "10"
        defaultEndMinute = "30"

        if defaults != {} and defaults is not None and 'withLectures' in defaults:
            
            if defaults['withLectures'] and weekday in defaults and defaults[weekday]['areThereLectures']:
                defaultCheck = True

                arrStart = defaults[weekday]['timeLectures']['timeStartDateLecture'].split(":")
                arrEnd = defaults[weekday]['timeLectures']['timeEndDateLecture'].split(":")

                defaultStartHour = arrStart[0] 
                defaultStartMinute = arrStart[1]
                defaultEndHour = arrEnd[0]
                defaultEndMinute = arrEnd[1]

        row = [
                sg.Text(weekdays_complete[x], size=(15, 1)), 
                sg.Checkbox("",key="CHECKBOX_"+(weekday), default=defaultCheck, enable_events=True),
                sg.Column([
                        [
                            sg.Combo([fromNumberToTime(x) for x in range(1, 24)], key="START_HOUR_"+(weekday), size=(3, 1), enable_events=True, default_value=defaultStartHour), 
                            sg.Text(':', size=(1, 1)),  
                            sg.Combo([fromNumberToTime(x) for x in range(0, 60)], key="START_MINUTE_"+(weekday), size=(3, 1), enable_events=True, default_value=defaultStartMinute), 
                            sg.Text('-', size=(1, 1)),  
                            sg.Combo([fromNumberToTime(x) for x in range(10, 24)], key="END_HOUR_"+(weekday), size=(3, 1), enable_events=True, default_value=defaultEndHour), 
                            sg.Text(':', size=(1, 1)),  
                            sg.Combo([fromNumberToTime(x) for x in range(0, 60)], key="END_MINUTE_"+(weekday), size=(3, 1), enable_events=True, default_value=defaultEndMinute)
                        ]
                    ],
                    visible=defaultCheck,
                    key="COLUMN_TIME_"+(weekday)
                )
            ] 
        rows.append(row)
    

    layout = [
        [sg.Input(disabled=True, key="startLectures", size=(10,1), default_text=defaultStartDate), sg.CalendarButton('Start lectures', no_titlebar=False, format="%Y-%m-%d", size=(15,1))],
        [sg.Input(disabled=True, key="endLectures", size=(10, 1), default_text=defaultEndDate), sg.CalendarButton('End lectures', no_titlebar=False, format="%Y-%m-%d", size=(15,1))],
        [rows],
        [sg.Button('Save', key="SAVE_SLOTS")]
    ]

    window = sg.Window("Set lecture slots", layout=layout, modal=True, finalize=True, keep_on_top=True)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event is not None:
            if event == "SAVE_SLOTS":
                

                sumOfLectures = 0

                for x in range(7):
                    if values["CHECKBOX_"+weekdays[x]]:
                        sumOfLectures += 1

                if sumOfLectures > 0:
                    infos['withLectures'] = True
                    infos['weekRepsLectures'] = ""
                
                    infos['startDateLectures'] = values['startLectures']
                    infos['endDateLectures'] = values["endLectures"]
                    for x in range(7):
                        infos[weekdays[x]] = {}
                        if values["CHECKBOX_"+weekdays[x]]:
                            infos[weekdays[x]]['areThereLectures'] = True
                            infos['weekRepsLectures'] += "1"
                            infos[weekdays[x]]['timeLectures']={
                                "timeStartDateLecture": values['START_HOUR_'+weekdays[x]]+":"+values['START_MINUTE_'+weekdays[x]],
                                "timeEndDateLecture": values['END_HOUR_'+weekdays[x]]+":"+values['END_MINUTE_'+weekdays[x]],
                                "durationLecture": (int(values['END_HOUR_'+weekdays[x]])*60 + int(values['END_MINUTE_'+weekdays[x]])) - (int(values['START_HOUR_'+weekdays[x]])*60 + int(values['START_MINUTE_'+weekdays[x]]))
                            }
                        else:
                            infos['weekReps'] += "0"
                            infos[weekdays[x]]['areThereLectures'] = False
                else:
                    infos['withLectures'] = False

                break


            if "CHECKBOX_" in event:
                eventKey = copy.copy(event)
                weekday = eventKey.replace("CHECKBOX_", "")

                window["COLUMN_TIME_"+weekday].update(visible=values[eventKey])


            if "START_HOUR_" in event or \
                "START_MINUTE_" in event or \
                "END_HOUR_" in event or \
                "END_MINUTE_" in event:

                eventKey = copy.copy(event)

                eventFocus = "START_HOUR_"
                if "START_MINUTE_" in event:
                    eventFocus = "START_MINUTE_"
                if "END_HOUR_" in event:
                    eventFocus = "END_HOUR_"
                if "END_MINUTE_" in event:
                    eventFocus = "END_MINUTE_"

                startHourKey = eventKey.replace(eventFocus, "START_HOUR_")
                startMinuteKey = eventKey.replace(eventFocus, "START_MINUTE_")
                endHourKey = eventKey.replace(eventFocus, "END_HOUR_")
                endMinuteKey = eventKey.replace(eventFocus, "END_MINUTE_")

                def getValues(values, key):
                    newVal = 0
                    if values[key] not in [None, ""]:
                        newVal = int(values[key])
                    return newVal
                
                startHour = getValues(values, startHourKey)
                startMinute = getValues(values, startMinuteKey)
                endHour = getValues(values, endHourKey)
                endMinute = getValues(values, endMinuteKey)

                if startHour > endHour:
                    newEndHour = min(startHour + 1, 23)
                    window[endHourKey].update(values=[fromNumberToTime(x) for x in range(startHour, 24)], value=fromNumberToTime(min(startHour + 1, 23)))

                    newStartMinute = 0
                    newEndMinute = 0

                    newMinRangeStart, newMaxRangeStart = 0, 60
                    newMinRangeEnd, newMaxRangeEnd = 0, 60
                    if newEndHour == startHour:
                        newStartMinute = 0
                        newEndMinute = 10
                        newMinRangeStart, newMaxRangeStart = 0, 10
                        newMinRangeEnd, newMaxRangeEnd = 10, 60

                    window[startMinuteKey].update(values=[fromNumberToTime(x) for x in range(newMinRangeStart, newMaxRangeStart)], value=fromNumberToTime(newStartMinute))
                    window[endMinuteKey].update(values=[fromNumberToTime(x) for x in range(newMinRangeEnd, newMaxRangeEnd)], value=fromNumberToTime(newEndMinute))
                else:
                    if startHour == endHour:
                        window[startMinuteKey].update(values=[fromNumberToTime(x) for x in range(0, endMinute)])

                        newStartMinute = max(endMinute - 1, 0)
                        if 0 <= startMinute < endMinute:
                            newStartMinute = startMinute

                        window[startMinuteKey].update(value=fromNumberToTime(newStartMinute))
                        window[endMinuteKey].update(values=[fromNumberToTime(x) for x in range(newStartMinute+1, 60)])
                        
                        newEndMinute = newStartMinute + 1
                        if newStartMinute + 1 <= endMinute < 60:
                            newEndMinute = endMinute
                        
                        window[endMinuteKey].update(value=fromNumberToTime(newEndMinute))

                    else:
                        window[endHourKey].update(values=[fromNumberToTime(x) for x in range(startHour, 24)], value=fromNumberToTime(endHour))
                        window[startMinuteKey].update(values=[fromNumberToTime(x) for x in range(0, 60)], value=fromNumberToTime(startMinute))
                        window[endMinuteKey].update(values=[fromNumberToTime(x) for x in range(0, 60)], value=fromNumberToTime(endMinute))
    
    window.close() 

    return infos

def getStudySlots(
        studyDays : str,
        arrAmount : str, 
        isBook : bool = True,
        isVideo : bool = False, 
        defaults : list | None = None, 
        sourceID : int|None = None
        ) -> list|None:
    
    comboSelection = ["Schematization", "Testing"]

    if isVideo:
        comboSelection.insert(0, "Viewing")

    if isBook:
        comboSelection.insert(0, "Reading")
    
    rows = []

    for x in range(7):
        if studyDays[x]:
            row = []

            for j in range(arrAmount[x]):
                defaultPages = 0
                defaultType = ""
                condType = False

                if isVideo:
                    defaultType = "Viewing"
                    condType = False

                if isBook:
                    defaultPages = "10"
                    defaultType = "Reading"
                    condType = True

                defaultDuration = 55
                
                if defaults and defaults is not None:
                    infos = copy.copy(defaults)

                    if 'areThereSessions' in defaults[weekdays[x]] and defaults[weekdays[x]]['areThereSessions'] and j < defaults[weekdays[x]]['amount']:
                    
                        defaultType = defaults[weekdays[x]]['types'][j]

                        if isBook:
                            defaultPages = defaults[weekdays[x]]['pages'][j]
                            defaultDuration = defaults[weekdays[x]]['durations'][j]
                            condType = True

                        if isVideo:
                            defaultDuration = defaults[weekdays[x]]['minutes'][j]
                            condType = False

                        if defaultType in ["Schematization"]:
                            condType = False
 
                lyt =   [
                            sg.Frame(str(f"{j+1}° Session"), [
                                [ sg.Text('Pages: ', size=(12, 1), visible=condType, key=f"TEXT_PAGES_{j}_SESSION_{weekdays[x]}"), sg.InputText(default_text=defaultPages, key=f'INPUT_TEXT_PAGES_{j}_SESSION_{weekdays[x]}', size=(5, 1), visible=condType)],
                                [ sg.Text('Type: ', size=(12, 1)), sg.Combo(comboSelection, size=(13, 1), default_value=defaultType, key=f'COMBO_TYPE_{j}_SESSION_{weekdays[x]}', enable_events=True)],
                                [ sg.Text('Duration: ', size=(12, 1)), sg.Combo([x for x in range(1, 61, 1)], default_value=defaultDuration, tooltip="Minutes", key=f'INPUT_TEXT_DURATION_{j}_SESSION_{weekdays[x]}', size=(3, 1), readonly=True)]
                            ])
                        ]
                
                row.append(lyt)

            frame = [sg.Frame(weekdays_complete[x], row)]
            rows.append(frame)
    
    column = sg.Column(rows, scrollable=True, vertical_scroll_only=True, size=(None, 350))

    layout = [
        [column],
        [sg.Button('Save', key="SAVE_SLOTS")]
    ]

    window = sg.Window("Set study slots", layout=layout, modal=True, finalize=True, keep_on_top=True)
    
    infos = {}

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event is not None:
            if "COMBO_TYPE_" in event:
                comboKey = copy.copy(event)
                condType = False
                if isBook and values[comboKey] in ["Reading", "Testing"]:
                    condType = True

                inputPagesKey = comboKey.replace("COMBO_TYPE_", "INPUT_TEXT_PAGES_")
                displayPagesKey = comboKey.replace("COMBO_TYPE_", "TEXT_PAGES_")
                
                window[displayPagesKey].update(visible=condType)
                window[inputPagesKey].update(visible=condType)


            if event == "SAVE_SLOTS":
                infos['totalPages'] = 0
                infos['totalMinutes'] = 0
                infos['totalDuration'] = 0
                infos['isBook'] = isBook

                maxStudyHour = getSettingsValue('maxStudyHour')
                
                condErrorHours = False
                condErrorHoursIndex = False
                errorTextHours = f"Max study hours allowed are {maxStudyHour}.\n"

                for x in range(7):
                    condErrorHoursIndex = False
                    infos[weekdays[x]] = {}
                    if studyDays[x]:
                        infos[weekdays[x]]['isStudyDay'] = True
                        infos[weekdays[x]]['areThereSessions'] = False
                        if arrAmount[x] > 0:
                            infos[weekdays[x]]['areThereSessions'] = True
                            infos[weekdays[x]]['amount'] = arrAmount[x]
                            infos[weekdays[x]]['types'] = []
                            infos[weekdays[x]]['durations'] = []
                            
                            if isBook:
                                infos[weekdays[x]]['pages'] = []
                                infos[weekdays[x]]['totalPages'] = 0

                            infos[weekdays[x]]['totalDuration'] = 0
                            for j in range(arrAmount[x]):
                                if isBook:
                                    pages = int(values[f'INPUT_TEXT_PAGES_{j}_SESSION_{weekdays[x]}'])
                                    typeStudy = values[f'COMBO_TYPE_{j}_SESSION_{weekdays[x]}']

                                    if typeStudy in ['Schematization']:
                                        pages = 0
                                    
                                    infos[weekdays[x]]['pages'].append(pages)
                                    infos[weekdays[x]]['totalPages'] += pages
                                    infos['totalPages'] += pages
                                else:
                                    minutes = int(values[f'INPUT_TEXT_DURATION_{j}_SESSION_{weekdays[x]}'])
                                    typeStudy = values[f'COMBO_TYPE_{j}_SESSION_{weekdays[x]}']

                                    if typeStudy in ['Schematization']:
                                        minutes = 0

                                    infos[weekdays[x]]['minutes'].append(minutes)
                                    infos[weekdays[x]]['totalMinutes'] += minutes
                                    infos['totalMinutes'] += minutes

                                duration = int(values[f'INPUT_TEXT_DURATION_{j}_SESSION_{weekdays[x]}'])
                                infos[weekdays[x]]['types'].append(values[f'COMBO_TYPE_{j}_SESSION_{weekdays[x]}'])
                                infos[weekdays[x]]['durations'].append(duration)
                                infos[weekdays[x]]['totalDuration'] += duration
                                infos['totalDuration'] += duration  

                                oldTotalMinutes = getTotalMinutes(x)
                                if sourceID is not None:
                                    oldTotalMinutes = getTotalMinutes(x, exceptID=sourceID)

                                newTotalMinutes = oldTotalMinutes + infos[weekdays[x]]['totalDuration']
                                totalHours = newTotalMinutes/60

                                if totalHours > maxStudyHour and not condErrorHoursIndex:
                                    condErrorHours = True
                                    condErrorHoursIndex = True
                                    errorTextHours += "You have to correct " + weekdays_complete[x] + " sessions. Your hour amounts is " + f'{totalHours:.2f}.\n'  
                    else:
                        infos[weekdays[x]]['isStudyDay'] = False
                
                if True in [condErrorHours]:
                    if condErrorHours:
                        sg.popup_error(errorTextHours, title="Too much hours", modal=True, keep_on_top=True)
                else:
                    break
                    
    
    window.close()
    return infos

