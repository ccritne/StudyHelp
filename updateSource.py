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
                        value=calculateDeadline(isBook=isBook, arrSessionWeek=studySlotsInfo, totalPages=numberPages, studiedPages=studiedPages))
            else:
                window['previewDeadline'].update(value='Check values!')

    if isVideo:
        durationMinutesStr = values['durationMinutes']
        viewedMinutesStr = values['viewedMinutes']
        
        if checkStrIntInput(viewedMinutesStr) and checkStrIntInput(durationMinutesStr):

            viewedMinutes = int(viewedMinutesStr)
            durationMinutes = int(durationMinutesStr)

            if durationMinutes > 0 and viewedMinutes >= 0:
                if studySlotsInfo is not None:
                    window['previewDeadline'].update(
                        value=calculateDeadline(isBook=isBook, isVideo=isVideo, arrSessionWeek=studySlotsInfo, totalMinutes=durationMinutes, viewedMinutes=viewedMinutes))
            else:
                window['previewDeadline'].update(value='Check values!')

def updateSource(command : str ="NEW"):

    studyDays = [bool(int(x)) for x in getSettingsValue('studyDays')]

    studySlotsInfo = None
    sourceSlotsInfo = None

    sourceValues = [None,"","100","0","", datetime.now().strftime('%Y-%m-%d'),"","", "30","0",datetime.now().strftime('%Y-%m-%d'),"0", ""]
    sessions = "0000000"
    
    buttonText = "ADD"
    windowTitle = "ADD NEW SOURCE"

    withLectures = False

    isBook = True
    isVideo = False

    defaultTotalPages = 100
    defaultStudiedPages = 0

    defaultTotalMinutes = 30
    defaultViewedMinutes = 0

    if command == "MODIFY":
        sourceValues = getSourceValues(getSelectedSourceID())
        studySlotsInfo = ast.literal_eval(sourceValues[6])

        sourceSlotsInfo = {}

        if sourceValues[2] is not None:
            defaultTotalPages = sourceValues[2]
    
        if sourceValues[3] is not None:
            defaultStudiedPages = sourceValues[3]

        if sourceValues[8] is not None:
            defaultTotalMinutes = sourceValues[8]

        if sourceValues[9] is not None:
            defaultViewedMinutes = sourceValues[9]

        sourceSlotsInfo['withLectures'] = studySlotsInfo['withLectures']
        if studySlotsInfo['withLectures']:
            sourceSlotsInfo['weekReps'] = studySlotsInfo['weekRepsLectures'] 
            sourceSlotsInfo['startDateLectures'] = studySlotsInfo['startDateLectures']
            sourceSlotsInfo['endDateLectures'] = studySlotsInfo['endDateLectures']
            for x in range(7):
                sourceSlotsInfo[weekdays[x]] = {}
                sourceSlotsInfo[weekdays[x]]['areThereLectures'] = studySlotsInfo[weekdays[x]]['areThereLectures']
                if studySlotsInfo[weekdays[x]]['areThereLectures']:
                    sourceSlotsInfo[weekdays[x]]['timeLectures'] = {
                        'timeStartDateLecture': studySlotsInfo[weekdays[x]]['timeLectures']['timeStartDateLecture'], 
                        'timeEndDateLecture': studySlotsInfo[weekdays[x]]['timeLectures']['timeEndDateLecture'], 
                        'durationLecture': studySlotsInfo[weekdays[x]]['timeLectures']['durationLecture']
                    }

        oldSessions = []
        for x in weekdays:
            if studySlotsInfo[x]['isStudyDay'] and studySlotsInfo[x]['areThereSessions']:
                oldSessions.append(str(studySlotsInfo[x]['amount']))
            else:
                oldSessions.append("0")

        isBook = True
        if sourceValues[11] is not None:
            isBook = sourceValues[11]
        isVideo = not isBook

        sessions = copy.copy(oldSessions)

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
        [sg.Text('Name '), sg.Input(key='nameDeck', default_text=sourceValues[1],expand_x=True)],
        [sg.Checkbox('Associate with lectures?', default=withLectures, key="checkboxLectures", enable_events=True), sg.Button('Insert slots', disabled= not withLectures, key="btnSlots")],
        [sg.Radio('Book', key="textSource", default=isBook, group_id="typeSource", enable_events=True), sg.Radio('Video', default=isVideo, enable_events=True, key="videoSource", group_id="typeSource")],
        [sg.HorizontalSeparator()],
        [
            sg.Column(columnGroup, justification="center")
        ],
        [sg.Button('Study slots', key="STUDY_SLOTS", expand_x=True)],
        [sg.HorizontalSeparator()],
        [sg.Text('Number of pages ', size=(20, 1), visible=isBook, key="textNumberPages"), sg.Input(key='numberPages', default_text=defaultTotalPages, justification="center", size=(4, 1), enable_events=True, visible=isBook)],
        [sg.Text('Total duration ', size=(20, 1), visible=isVideo, key="textTotalDuration"), sg.Input(key='durationMinutes', tooltip="Duration in minutes", default_text=defaultTotalMinutes, justification="center", size=(5, 1), enable_events=True, visible=isVideo)],
        
        [sg.Text('Number of studied pages ', size=(20, 1), visible=isBook, key="textStudiedPages"), sg.Input(key='entryStudiedPages', default_text=defaultStudiedPages, justification="center", size=(4, 1), enable_events=True, visible=isBook)],
        [sg.Text('Minutes of see view ', size=(20, 1), visible=isVideo, key="textMinutesViewed"), sg.Input(key='viewedMinutes', tooltip="Duration in minutes", default_text=defaultViewedMinutes, justification="center", size=(5, 1), enable_events=True, visible=isVideo)],
        
        [sg.Text('Document ', size=(20, 1)), sg.Input(key="pathSource", size=(10, 1), default_text=sourceValues[4]), sg.FileBrowse(file_types=(('Portable Document Format', 'PDF'),), visible=isBook)],
        [sg.Text('Url ', size=(20, 1), visible=isVideo, key="urlVideo"), sg.Input(key="pathVideo", size=(30, 1), expand_x=True, default_text=sourceValues[7], visible=isVideo)],
        
        [sg.Text('Deadline ', size=(20, 1)), sg.Input(key="previewDeadline", size=(13, 1), default_text=sourceValues[5], readonly=True)],
        [sg.Button(buttonText, key="updateSource", expand_x=True)]
    ]

    window = sg.Window(windowTitle, layout=layout, modal=True, finalize=True, keep_on_top=True)

    window['textNumberPages'].update(visible=isBook)
    window['numberPages'].update(visible=isBook)
    window['textTotalDuration'].update(visible=isVideo)
    window['durationMinutes'].update(visible=isVideo)

    window['textStudiedPages'].update(visible=isBook)
    window['entryStudiedPages'].update(visible=isBook)
    window['textMinutesViewed'].update(visible=isVideo)
    window['viewedMinutes'].update(visible=isVideo)

    window['urlVideo'].update(visible=isVideo)
    window['pathVideo'].update(visible=isVideo)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event is not None:
            if event in ['numberPages', 'studiedPages', 'durationMinutes', 'viewedMinutes']:
                isBook = bool(values['textSource'])
                updateDeadline(isBook=isBook, isVideo=isVideo, window=window, values=values, studySlotsInfo=studySlotsInfo)

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

                    if sourceSlotsInfo is not None:
                        studySlotsInfo['withLectures'] = sourceSlotsInfo['withLectures']
                        if sourceSlotsInfo['withLectures']:
                            studySlotsInfo['weekRepsLectures'] = sourceSlotsInfo['weekReps']
                            studySlotsInfo['startDateLectures'] = sourceSlotsInfo['startDateLectures']
                            studySlotsInfo['endDateLectures'] = sourceSlotsInfo['endDateLectures']
                            for x in range(7):
                                studySlotsInfo[weekdays[x]]['areThereLectures'] = sourceSlotsInfo[weekdays[x]]['areThereLectures']
                                if weekdays[x] in sourceSlotsInfo and sourceSlotsInfo[weekdays[x]]['areThereLectures']:
                                    studySlotsInfo[weekdays[x]]['timeLectures'] = {
                                        'timeStartDateLecture': sourceSlotsInfo[weekdays[x]]['timeLectures']['timeStartDateLecture'], 
                                        'timeEndDateLecture': sourceSlotsInfo[weekdays[x]]['timeLectures']['timeEndDateLecture'], 
                                        'durationLecture': sourceSlotsInfo[weekdays[x]]['timeLectures']['durationLecture']
                                    }

                    updateDeadline(isBook=isBook, window=window, values=values, studySlotsInfo=studySlotsInfo)

                    for x in range(7):
                        if studySlotsInfo[weekdays[x]]['isStudyDay'] and studySlotsInfo[weekdays[x]]['areThereSessions']:
                            maxStudyHour = getSettingsValue('maxStudyHour')
                            totalMinutes = getTotalMinutes(x, exceptID=getSelectedSourceID()) + studySlotsInfo[weekdays[x]]['totalDuration']
                            remainingMinutes = maxStudyHour*60 - totalMinutes 

                            window['DISPLAY_TIME_REMAINING_'+weekdays[x]].update(value=remainingMinutes)

                else:
                    sg.popup_ok('Insert almost one session!', title="WARNING", keep_on_top=True, modal=True)

            if event in ['textSource', 'videoSource']:
                if event in ['textSource', 'videoSource']:
                    if event == 'textSource':
                        isBook = True
                        isVideo = False

                    if event == 'videoSource':
                        isVideo = True
                        isBook = False

                    ### !!! Fixing the visible and values

                    window['textNumberPages'].update(visible=isBook)
                    window['numberPages'].update(visible=isBook)
                    window['textTotalDuration'].update(visible=isVideo)
                    window['durationMinutes'].update(visible=isVideo)

                    window['textStudiedPages'].update(visible=isBook)
                    window['entryStudiedPages'].update(visible=isBook)
                    window['textMinutesViewed'].update(visible=isVideo)
                    window['viewedMinutes'].update(visible=isVideo)

                    window['urlVideo'].update(visible=isVideo)
                    window['pathVideo'].update(visible=isVideo)
            
            if event == "updateSource":
  
                nameBook = values['nameDeck']
                
                if isVideo:
                    query = 'INSERT INTO sources(name, arrSessions, deadline, url, durationMinutes, viewedMinutes, insertDate) VALUES (?, ?, ?, ?, ?, ?, ?)'
                    if command == "MODIFY":
                        query = 'UPDATE sources SET name = ?, arrSessions = ?, deadline = ?, url = ?, durationMinutes = ?, viewedMinutes = ? WHERE ID = ?'

                    url = values['pathVideo']

                    durationMinutesStr = values['durationMinutes']
                    viewedMinutesStr = values['viewedMinutes']
                    
                    if checkStrIntInput(viewedMinutesStr) and checkStrIntInput(durationMinutesStr):

                        viewedMinutes = int(viewedMinutesStr)
                        durationMinutes = int(durationMinutesStr)

                        if durationMinutes > 0 and viewedMinutes >= 0:
                            if studySlotsInfo is not None:
                                
                                deadline = calculateDeadline(isBook=isBook, isVideo=isVideo, arrSessionWeek=studySlotsInfo, totalMinutes=durationMinutes, viewedMinutes=viewedMinutes)

                                parameters = (nameBook, str(studySlotsInfo), deadline, url, durationMinutes, viewedMinutes)

                                if command == 'MODIFY':
                                    parameters = parameters + (getSelectedSourceID(), )

                                if command == "NEW":
                                    parameters = parameters + (datetime.now().strftime('%Y-%m-%d'), )

                                                            
                                cursor.execute(query, parameters)
                                con.commit()
                                break
                            else:
                                    sg.popup_ok('You have to set your study slots!', title="WARNING", keep_on_top=True, modal=True)
                        else:
                            sg.popup_ok('Please, set the correct values!', title="WARNING", keep_on_top=True, modal=True)
                    else:
                        sg.popup_ok('Please, set the correct values!', title="WARNING", keep_on_top=True, modal=True)

                if isBook:
                    query = 'INSERT INTO sources(name, numberPages, studiedPages, filename, arrSessions, deadline, insertDate) VALUES (?, ?, ?, ?, ?, ?, ?)'
                    if command == "MODIFY":
                        query = 'UPDATE sources SET name = ?, numberPages = ?, studiedPages = ?, filename = ?, arrSessions = ?, deadline = ? WHERE ID = ?'

                    numberPagesStr = values['numberPages']
                    studiedPagesStr = values['entryStudiedPages']
                    
                    filename = values['pathSource']
                    
                    if checkStrIntInput(numberPagesStr) and checkStrIntInput(studiedPagesStr):

                        numberPages = int(numberPagesStr)
                        studiedPages = int(studiedPagesStr)

                        if numberPages > 0 and studiedPages >= 0:
                            if studySlotsInfo is not None:
                                
                                deadline = calculateDeadline(isBook=isBook, arrSessionWeek=studySlotsInfo, totalPages=numberPages, studiedPages=studiedPages)

                                parameters = (nameBook, numberPages, studiedPages, filename, str(studySlotsInfo), deadline)

                                if command == 'MODIFY':
                                    parameters = parameters + (getSelectedSourceID(), )

                                if command == "NEW":
                                    parameters = parameters + (datetime.now().strftime('%Y-%m-%d'), )

                                cursor.execute(query, parameters)
                                con.commit()
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

            if event == "btnSlots":
                sourceSlotsInfo = getSourceSlots(sourceSlotsInfo)

                if studySlotsInfo is None:
                    studySlotsInfo = {}

                studySlotsInfo['withLectures'] = sourceSlotsInfo['withLectures']
                if sourceSlotsInfo['withLectures']:
                    studySlotsInfo['weekRepsLectures'] = sourceSlotsInfo['weekReps']
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