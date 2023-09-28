from functions import *
from studySlots import *
from setup import weekdays

def updateDeadline(
        window : sg.Window, 
        values : dict, 
        studySlotsInfo : dict,
        isBook : bool = True, 
        isVideo : bool = False
        ):
    if isBook:
        numberPagesStr = values['numberPages']
        studiedPagesStr = values['entryStudiedPages']
        if checkStrIntInput(numberPagesStr) and checkStrIntInput(studiedPagesStr):
            numberPages = int(numberPagesStr)
            studiedPages = int(studiedPagesStr)
            if numberPages > 0 and studiedPages >= 0:
                if studySlotsInfo is not None:
                    window['previewDeadline'].update(
                        value=getStringDate(calculateDeadline(isBook=isBook, arrSessionWeek=studySlotsInfo, totalPages=numberPages, studiedPages=studiedPages)))
            else:
                window['previewDeadline'].update(value='Check values!')

def creationEvents(
        command : str, 
        studySlotsInfo : list, 
        lastPage : int,
        withLectures : bool,
        deadline : datetime
        ):
    ### Creation of events
    lastID = None

    if command == "NEW":
        lastID = cursor.execute('SELECT MAX(ID) FROM SOURCES').fetchone()[0]

    if command == "MODIFY": 
        # Deletion of future events
        lastID = getSelectedSourceID()
        iterDay = datetime.now()
        sql = "DELETE FROM calendar WHERE date >= ? AND sourceID = ?"
        parameters = (getStringDate(iterDay), lastID)
        cursor.execute(sql, parameters)
        con.commit()
        
    iterDay = datetime.now()
    insertDate = getStringDate(datetime.now())
    days = (deadline - iterDay).days + 1
    iter = 0
    indexWeek = datetime.now().weekday()
    sql = "INSERT INTO CALENDAR(type, insertedDay, date, startSession, endSession, sourceID) VALUES \n"

    while iter <= days:
        if studySlotsInfo[weekdays[indexWeek]]['isStudyDay'] and studySlotsInfo[weekdays[indexWeek]]['areThereSessions']: 
            iterDayStr = getStringDate(iterDay)
            for x in range(studySlotsInfo[weekdays[indexWeek]]['amount']):
                studyType = studySlotsInfo[weekdays[indexWeek]]['types'][x]
                
                sql += "('"+studyType+"', '"+insertDate+"', '"+iterDayStr+"'"
                
                startPage = lastPage
                endPage = startPage + studySlotsInfo[weekdays[indexWeek]]['pages'][x]
                lastPage = endPage

                if  studyType in ["Schematization"]:
                    startPage = "NULL"
                    endPage = "NULL"

                sql += ", "+str(startPage)+", "+str(endPage)+", "+str(lastID)+"),"

        indexWeek += 1
        
        if indexWeek == 7:
            indexWeek = 0

        iter += 1
        
        iterDay += timedelta(days=1)
    
    
    sql = sql[:len(sql) - 1] + ';'

    cursor.execute(sql)
    con.commit()

    if withLectures:
        sql = 'INSERT INTO calendar(type, insertedDay, date, timeStartDate, timeEndDate, sourceID) VALUES \n'
        iterDay = datetime.strptime(studySlotsInfo['startDateLectures'], '%Y-%m-%d')
        insertDate = getStringDate(datetime.now())
        deadlineLectures = studySlotsInfo['endDateLectures']
        days = (datetime.strptime(deadlineLectures, '%Y-%m-%d') - iterDay).days
        iter = 0
        indexWeek = iterDay.weekday()

        while iter <= days:
            if studySlotsInfo[weekdays[indexWeek]]['areThereLectures']:
                sql += "('Lecture', '"+insertDate+"','"+getStringDate(iterDay)+"', '"+studySlotsInfo[weekdays[indexWeek]]['timeLectures']['timeStartDateLecture']+"', '"+studySlotsInfo[weekdays[indexWeek]]['timeLectures']['timeEndDateLecture']+"', "+str(lastID)+"),"

            indexWeek += 1

            if indexWeek == 7:
                indexWeek = 0

            iter += 1
            
            iterDay += timedelta(days=1)

        sql = sql[:len(sql)-1] + ";"
        cursor.execute(sql)
        con.commit()

def updateSource(command : str ="NEW"):

    studyDays = [bool(int(x)) for x in getSettingsValue('studyDays')]

    studySlotsInfo = {}

    defaultName = ""

    defaultTodayDateStr = datetime.now().strftime('%Y-%m-%d')
    
    sessions = ""
    
    buttonText = "ADD"
    windowTitle = "ADD NEW SOURCE"

    withLectures = False
    defaultNameCourse = ""

    isBook = True
    isVideo = False

    defaultTotalPages = 100
    defaultStudiedPages = 0

    defaultTotalMinutes = 30
    defaultViewedMinutes = 0

    defaultPathfile = ""
    defaultUrl = ""

    defaultDeadline = "Insert sessions!"

    if command == "MODIFY":
        sourceValues = getSourceValues(getSelectedSourceID())

        studySlotsInfo = ast.literal_eval(sourceValues[7])
        
        def updateDefaultValue(oldValue, sourceValues, index):
            if sourceValues[index] is not None:
                return sourceValues[index]
            
            return oldValue
            
        defaultNameCourse = updateDefaultValue(defaultNameCourse, sourceValues, 1)
        
        defaultName = updateDefaultValue(defaultName, sourceValues, 2)
        defaultTotalPages = updateDefaultValue(defaultName, sourceValues, 3)
        defaultStudiedPages = updateDefaultValue(defaultStudiedPages, sourceValues, 4)
        defaultPathfile = updateDefaultValue(defaultPathfile, sourceValues, 5)
        defaultDeadline = updateDefaultValue(defaultDeadline, sourceValues, 6)

        for x in range(7):
            if studySlotsInfo[weekdays[x]]['isStudyDay'] and studySlotsInfo[weekdays[x]]['areThereSessions']:
                sessions += str(studySlotsInfo[weekdays[x]]['amount'])
            else:
                sessions += "0"


        withLectures = studySlotsInfo['withLectures']
        
        buttonText = "MODIFY"
        windowTitle = "MODIFY BOOK"

    columnGroup = [
        [
            sg.Text('Day', size=(5, 1), justification="center"), 
            sg.Text('Sessions', size=(10, 1), justification="center"), 
            sg.Text('Minutes left', size=(10, 1), justification="center")
        ]
    ]
    
    for x in range(7):
        if studyDays[x]:
            maxStudyHour = getSettingsValue('maxStudyHour')
            totalMinutes = getTotalMinutes(x)
            remainingMinutes = maxStudyHour*60 - totalMinutes
            
            row = [
                    sg.Text(text=weekdays[x], size=(5, 1)), 
                    sg.InputText(
                        size=(10, 1), 
                        justification="center", 
                        default_text=sessions[x], 
                        enable_events=True, 
                        key='INPUT_TEXT_SESSIONS_'+weekdays[x], 
                        ),
                    sg.Text(text=remainingMinutes, size=(10, 1), justification="center", key="DISPLAY_TIME_REMAINING_"+weekdays[x]),
                ]
            columnGroup.append(row)

    layout = [
        [sg.Text('Name '), sg.Input(key='nameDeck', default_text=defaultName,expand_x=True)],
        [sg.Checkbox('Associate with lectures?', default=withLectures, key="checkboxLectures", enable_events=True), sg.Text('Name course: ', key="DISPLAY_TEXT_NAME_COURSE", visible=withLectures), sg.Input(key="INPUT_TEXT_NAME_COURSE", default_text=defaultNameCourse, visible=withLectures), sg.Button('Insert slots', disabled= not withLectures, key="btnSlots")],
        [sg.HorizontalSeparator()],
        [
            sg.Column(columnGroup, justification="center")
        ],
        [sg.Button('Study slots', key="STUDY_SLOTS", expand_x=True)],
        [sg.HorizontalSeparator()],
        [sg.Text('Number of pages ', size=(20, 1), visible=isBook, key="textNumberPages"), sg.Input(key='numberPages', default_text=defaultTotalPages, justification="center", size=(4, 1), enable_events=True, visible=isBook)],
        
        [sg.Text('Number of studied pages ', size=(20, 1), visible=isBook, key="textStudiedPages"), sg.Input(key='entryStudiedPages', default_text=defaultStudiedPages, justification="center", size=(4, 1), enable_events=True, visible=isBook)],
        
        [sg.Text('Document ', size=(20, 1)), sg.Input(key="pathSource", size=(10, 1), default_text=defaultPathfile), sg.FileBrowse(file_types=(('Portable Document Format', 'PDF'),), visible=isBook)],
        
        [sg.Text('Deadline ', size=(20, 1)), sg.Input(key="previewDeadline", size=(10, 1), default_text=defaultDeadline, readonly=True)],
        [sg.Button(buttonText, key="updateSource", expand_x=True)]
    ]

    window = sg.Window(windowTitle, layout=layout, modal=True, finalize=True, keep_on_top=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event is not None:
            if event in ['numberPages', 'studiedPages'] and studySlotsInfo != {}:
                updateDeadline(isBook=isBook, window=window, values=values, studySlotsInfo=studySlotsInfo)

            if event == "STUDY_SLOTS":
                arrAmounts = []
                bookStudyDays = []

                sumOfAmount = 0

                for x in range(7):
                    if studyDays[x]:
                        amount = int(values[f"INPUT_TEXT_SESSIONS_{weekdays[x]}"])
                        arrAmounts.append(amount)
                        bookStudyDays.append(True)
                        sumOfAmount += amount
                    else:
                        arrAmounts.append(0)
                        bookStudyDays.append(False)
                
                if sumOfAmount > 0:
                    if command == "NEW":
                        studySlotsInfo = getStudySlots(isBook=isBook, isVideo=isVideo, studyDays=bookStudyDays, arrAmount=arrAmounts, defaults=studySlotsInfo)
                    if command == "MODIFY":
                        studySlotsInfo = getStudySlots(isBook=isBook, isVideo=isVideo, studyDays=bookStudyDays, arrAmount=arrAmounts, defaults=studySlotsInfo, sourceID=getSelectedSourceID())

                    updateDeadline(isBook=isBook, window=window, values=values, studySlotsInfo=studySlotsInfo)

                    for x in range(7):
                        if studySlotsInfo[weekdays[x]]['isStudyDay'] and studySlotsInfo[weekdays[x]]['areThereSessions']:
                            maxStudyHour = getSettingsValue('maxStudyHour')
                            totalMinutes = getTotalMinutes(x, exceptID=getSelectedSourceID()) + studySlotsInfo[weekdays[x]]['totalDuration']
                            remainingMinutes = maxStudyHour*60 - totalMinutes 

                            window['DISPLAY_TIME_REMAINING_'+weekdays[x]].update(value=remainingMinutes)

                else:
                    sg.popup_ok('Insert almost one session!', title="WARNING", keep_on_top=True, modal=True)

            if event == "updateSource":
  
                nameBook = values['nameDeck']
                courseName = values['INPUT_TEXT_NAME_COURSE']

                if isBook:
                    query = 'INSERT INTO sources(name, courseName, numberPages, studiedPages, filename, arrSessions, deadline, insertDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                    if command == "MODIFY":
                        query = 'UPDATE sources SET name = ?, courseName = ?, numberPages = ?, studiedPages = ?, filename = ?, arrSessions = ?, deadline = ? WHERE ID = ?'

                    numberPagesStr = values['numberPages']
                    studiedPagesStr = values['entryStudiedPages']
                    
                    filename = values['pathSource']

                    if checkStrIntInput(numberPagesStr) and checkStrIntInput(studiedPagesStr):

                        numberPages = int(numberPagesStr)
                        studiedPages = int(studiedPagesStr)

                        if numberPages > 0 and studiedPages >= 0:
                            if studySlotsInfo != {}:
                                
                                deadline = calculateDeadline(isBook=isBook, arrSessionWeek=studySlotsInfo, totalPages=numberPages, studiedPages=studiedPages)

                                parameters = (nameBook, courseName, numberPages, studiedPages, filename, str(studySlotsInfo), deadline)

                                if command == 'MODIFY':
                                    parameters = parameters + (getSelectedSourceID(), )

                                if command == "NEW":
                                    parameters = parameters + (defaultTodayDateStr, )

                                cursor.execute(query, parameters)
                                con.commit()

                                lastPage = studiedPages + 1

                                creationEvents(command=command, studySlotsInfo=studySlotsInfo, lastPage=lastPage, withLectures=withLectures, deadline=deadline)

                                break
                            else:
                                sg.popup_ok('You have to set your study slots!', title="WARNING", keep_on_top=True, modal=True)
                        else:
                            sg.popup_ok('Please, set the correct values!', title="WARNING", keep_on_top=True, modal=True)
                    else:
                        sg.popup_ok('Please, set the correct values!', title="WARNING", keep_on_top=True, modal=True)
    
            if event == "checkboxLectures":
                withLectures = values['checkboxLectures']
                window['btnSlots'].update(disabled = not withLectures)
                window['DISPLAY_TEXT_NAME_COURSE'].update(visible = withLectures)
                window['INPUT_TEXT_NAME_COURSE'].update(visible = withLectures)

            if event == "btnSlots":
                sourceSlotsInfo = getSourceSlots(studySlotsInfo)

                studySlotsInfo['withLectures'] = sourceSlotsInfo['withLectures']
                if studySlotsInfo['withLectures']:
                    studySlotsInfo['weekRepsLectures'] = sourceSlotsInfo['weekRepsLectures']
                    studySlotsInfo['startDateLectures'] = sourceSlotsInfo['startDateLectures']
                    studySlotsInfo['endDateLectures'] = sourceSlotsInfo['endDateLectures']
                    for x in range(7):
                        if weekdays[x] not in studySlotsInfo:
                            studySlotsInfo[weekdays[x]] = {}

                        studySlotsInfo[weekdays[x]]['areThereLectures'] = sourceSlotsInfo[weekdays[x]]['areThereLectures']

                        if weekdays[x] in sourceSlotsInfo and sourceSlotsInfo[weekdays[x]]['areThereLectures']:
                            studySlotsInfo[weekdays[x]]['timeLectures'] = {
                                'timeStartDateLecture': sourceSlotsInfo[weekdays[x]]['timeLectures']['timeStartDateLecture'], 
                                'timeEndDateLecture': sourceSlotsInfo[weekdays[x]]['timeLectures']['timeEndDateLecture'], 
                                'durationLecture': sourceSlotsInfo[weekdays[x]]['timeLectures']['durationLecture']
                            }


    window.close()