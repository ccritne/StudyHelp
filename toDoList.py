from functions import *

def previewEvent(informations : list):
    ID = informations[0]
    title = informations[10]
    type = informations[1]
    startTime = informations[5]
    endTime = informations[6]
    startSession = informations[7]
    endSession = informations[8]
    
    arrStart = ["", ""]
    if startTime not in ["", None]:
        arrStart = startTime.split(':')

    defaultStartHour = arrStart[0]
    defaultStartMinute = arrStart[1]

    arrEnd = ["", ""]
    if endTime not in ["", None]:
        arrEnd = endTime.split(':')

    defaultEndHour = arrEnd[0]
    defaultEndMinute = arrEnd[1]
    
    layout = [
        [
            [
                sg.Combo([fromNumberToTime(x) for x in range(1, 24)], key="START_HOUR", size=(3, 1), enable_events=True, default_value=defaultStartHour), 
                sg.Text(':', size=(1, 1)),  
                sg.Combo([fromNumberToTime(x) for x in range(0, 60)], key="START_MINUTE", size=(3, 1), enable_events=True, default_value=defaultStartMinute), 
                sg.Text('-', size=(1, 1)),  
                sg.Combo([fromNumberToTime(x) for x in range(10, 24)], key="END_HOUR", size=(3, 1), enable_events=True, default_value=defaultEndHour), 
                sg.Text(':', size=(1, 1)),  
                sg.Combo([fromNumberToTime(x) for x in range(0, 60)], key="END_MINUTE", size=(3, 1), enable_events=True, default_value=defaultEndMinute)
            ],
            [sg.Text('')]
            [sg.HorizontalSeparator()],
            [sg.Button('Save', key="SAVE_EVENT")]

        ],
    ]

    window =  sg.Window(title="Preview", layout=layout, finalize=True, modal=True, keep_on_top=True)


    while True:
        
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event is not None:

            if "START_HOUR" in event or \
                "START_MINUTE" in event or \
                "END_HOUR" in event or \
                "END_MINUTE" in event:

                eventKey = copy.copy(event)

                eventFocus = "START_HOUR"
                if "START_MINUTE" in event:
                    eventFocus = "START_MINUTE"
                if "END_HOUR" in event:
                    eventFocus = "END_HOUR"
                if "END_MINUTE" in event:
                    eventFocus = "END_MINUTE"

                startHourKey = eventKey.replace(eventFocus, "START_HOUR")
                startMinuteKey = eventKey.replace(eventFocus, "START_MINUTE")
                endHourKey = eventKey.replace(eventFocus, "END_HOUR")
                endMinuteKey = eventKey.replace(eventFocus, "END_MINUTE")

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

def seeToDoList():
    if getSelectedDate() is None:
        dt = datetime.combine(datetime.now(), time(0, 0))
        setSelectedDate(dt)

    def getToDoDataOf(date : datetime):
        dateStr = getStringDate(date)
        query = f'''SELECT calendar.ID, 
                            sources.courseName,
                            sources.name, 
                            calendar.type,
                            calendar.description,
                            calendar.timeStartDate,
                            calendar.timeEndDate,
                            calendar.startSession,
                            calendar.endSession
                    FROM calendar 
                    LEFT JOIN 
                    sources ON sourceID = sources.ID 
                    WHERE date = ? 
                    ORDER BY insertedDay
                '''
        parameters = (dateStr, )

        cursor.execute(query, parameters)
        result = cursor.fetchall()
        
        rows = []
        for x in range(len(result)):
            row = [result[x][0], "", "", "", "", "", "", "", ""]
            for j in range(1, len(result[x])):
                if result[x][j] is not None:
                    row[j] = result[x][j]
            rows.append(row)

        return rows
    
    todoList = getToDoDataOf(getSelectedDate())
    
    layout = [
                [sg.InputText(key="selectedDate", default_text=getStringDate(getSelectedDate()), size=(10, 1)), sg.Button('Select day', key='selectToDoDate')],
                [
                    sg.Table(
                            values=todoList,
                            headings=["ID", "Course", "Source Title", "Type", "Description", "Start", "End", "Start session", "End session"], 
                            key="To-Do-List",
                            auto_size_columns=False,
                            expand_y=True, 
                            expand_x=True,
                            col_widths=[5, 15, 15, 10, 10, 5, 5, 10, 10],
                            justification="center",
                            enable_click_events=True
                        )
                ]
            ]
    
    window =  sg.Window(title="TODO List", layout=layout, finalize=True, modal=True, keep_on_top=True)

    window['selectedDate'].bind("<Return>", "_Enter")

    while True:
        
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        
        if event is not None: 
            if event[1] == '+CLICKED+' and (event[2][0] is not None and event[2][0] >=0):
                informations = todoList[event[2][0]]
                previewEvent(informations)

            if event in ["selectToDoDate", 'selectedDate_Enter']:
                sDate = values['selectedDate']

                if event == 'selectToDoDate':
                    dtMon = datetime.now().month
                    selectedDate = sg.popup_get_date(close_when_chosen=True, start_mon=dtMon, no_titlebar=False, modal=True, keep_on_top=True)
                    sDate = fromNumberToTime(selectedDate[2])+"-"+fromNumberToTime(selectedDate[0])+"-"+fromNumberToTime(selectedDate[1])

                setSelectedDate(datetime.strptime(sDate, '%Y-%m-%d'))

                window['selectedDate'].update(value=getStringDate(getSelectedDate()))
                todoList = getToDoDataOf(getSelectedDate())
                window['To-Do-List'].update(values=todoList)
    
    window.close()
