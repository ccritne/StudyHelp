from functions import *
from studySlots import getStudySlots
from setup import weekdays

def updateDeadline(window, values, studySlotsInfo):
    numberPagesStr = values['numberPages']
    studiedPagesStr = values['entryStudiedPages']
    if checkStrIntInput(numberPagesStr) and checkStrIntInput(studiedPagesStr):
        numberPages = int(numberPagesStr)
        studiedPages = int(studiedPagesStr)
        if numberPages > 0 and studiedPages >= 0:
            if studySlotsInfo is not None:
                window['previewDeadline'].update(value=calculateDeadline(arrSessionWeek=studySlotsInfo, totalPages=numberPages, studiedPages=studiedPages))
        else:
            window['previewDeadline'].update(value='Check values!')

def updateSource(command="NEW", sourceID=None):

    studyDays = [bool(int(x)) for x in getSettingsValue('studyDays')]

    studySlotsInfo = None

    sourceValues = [None,"","100","0","", datetime.now().strftime('%Y-%m-%d'),"",""]
    sessions = [0, 0, 0, 0, 0, 0, 0]
    
    buttonText = "ADD"
    windowTitle = "ADD NEW SOURCE"

    isBook = True
    isVideo = False

    query = 'INSERT INTO sources(name, numberPages, studiedPages, filename, arrSessions, deadline, insertDate) VALUES (?, ?, ?, ?, ?, ?, ?)'

    if command == "modify":
        sourceValues = getSourceValues(getSelectedSourceID())
        studySlotsInfo = ast.literal_eval(sourceValues[6])
        oldSessions = []
        for x in weekdays:
            if studySlotsInfo[x]['isStudyDay']:
                oldSessions.append(str(studySlotsInfo[x]['amount']))
            else:
                oldSessions.append("0")

        isBook = sourceValues[11]
        isVideo = not isBook

        sessions = copy.copy(oldSessions)
        
        
        query = 'UPDATE sources SET name = ?, numberPages = ?, studiedPages = ?, filename = ?, arrSessions = ?, deadline = ? WHERE ID = ?'
        
        if not isBook:
            query = 'UPDATE sources SET name = ?, arrSessions = ?, deadline = ?, url = ?, durationMinutes = ?, viewedMinutes = ? WHERE ID = ?'

        buttonText = "MODIFY"
        windowTitle = "MODIFY BOOK"

    

    layout = [
        [sg.Text('Name '), sg.Input(key='nameDeck', default_text=sourceValues[1],expand_x=True)],
        [sg.Radio('Book', key="textSource", default=True, group_id="typeSource", enable_events=True), sg.Radio('Video', enable_events=True, key="videoSource", group_id="typeSource")],
        [sg.HorizontalSeparator()],
        [
            sg.Column([
                    [sg.Text('Day', size=(5, 1)), sg.Text('Sessions', size=(10, 1))],
                    [sg.Text('Mon', size=(5, 1), visible=studyDays[0]), sg.InputText(size=(5, 1), justification="center", default_text=sessions[0], enable_events=True, key='INPUT_TEXT_SESSIONS_MON', visible=studyDays[0])],
                    [sg.Text('Tue', size=(5, 1), visible=studyDays[1]), sg.InputText(size=(5, 1), justification="center", default_text=sessions[1], enable_events=True, key='INPUT_TEXT_SESSIONS_TUE', visible=studyDays[1])],
                    [sg.Text('Wed', size=(5, 1), visible=studyDays[2]), sg.InputText(size=(5, 1), justification="center", default_text=sessions[2], enable_events=True, key='INPUT_TEXT_SESSIONS_WED', visible=studyDays[2])],
                    [sg.Text('Thu', size=(5, 1), visible=studyDays[3]), sg.InputText(size=(5, 1), justification="center", default_text=sessions[3], enable_events=True, key='INPUT_TEXT_SESSIONS_THU', visible=studyDays[3])],
                    [sg.Text('Fri', size=(5, 1), visible=studyDays[4]), sg.InputText(size=(5, 1), justification="center", default_text=sessions[4], enable_events=True, key='INPUT_TEXT_SESSIONS_FRI', visible=studyDays[4])],
                    [sg.Text('Sat', size=(5, 1), visible=studyDays[5]), sg.InputText(size=(5, 1), justification="center", default_text=sessions[5], enable_events=True, key='INPUT_TEXT_SESSIONS_SAT', visible=studyDays[5])],
                    [sg.Text('Sun', size=(5, 1), visible=studyDays[6]), sg.InputText(size=(5, 1), justification="center", default_text=sessions[6], enable_events=True, key='INPUT_TEXT_SESSIONS_SUN', visible=studyDays[6])],
            ], justification="center")
        ],
        [sg.Button('Study slots', key="STUDY_SLOTS", expand_x=True)],
        [sg.HorizontalSeparator()],
        [sg.Text('Number of pages ', size=(20, 1), visible=isBook, key="textNumberPages"), sg.Input(key='numberPages', default_text=sourceValues[2], justification="center", size=(4, 1), enable_events=True, visible=isBook)],
        [sg.Text('Total duration ', size=(20, 1), visible=isVideo, key="textTotalDuration"), sg.Input(key='durationMinutes', tooltip="Duration in minutes", default_text=sourceValues[7], justification="center", size=(5, 1), enable_events=True, visible=isVideo)],
        
        [sg.Text('Number of studied pages ', size=(20, 1), visible=isBook, key="textStudiedPages"), sg.Input(key='entryStudiedPages', default_text=sourceValues[3], justification="center", size=(4, 1), enable_events=True, visible=isBook)],
        [sg.Text('Minutes of see view ', size=(20, 1), visible=isVideo, key="textMinutesViewed"), sg.Input(key='viewedMinutes', tooltip="Duration in minutes", default_text=sourceValues[7], justification="center", size=(5, 1), enable_events=True, visible=isVideo)],
        
        [sg.Text('Document ', size=(20, 1)), sg.Input(key="pathSource", size=(10, 1), default_text=sourceValues[4]), sg.FileBrowse(file_types=(('Portable Document Format', 'PDF'),), visible=isBook)],
        [sg.Text('Url ', size=(20, 1), visible=isVideo, key="urlVideo"), sg.Input(key="pathVideo", size=(30, 1), expand_x=True, default_text=sourceValues[4], visible=isVideo)],
        
        [sg.Text('Deadline ', size=(20, 1)), sg.Input(key="previewDeadline", size=(13, 1), default_text=sourceValues[5], readonly=True)],
        [sg.Button(buttonText, key="updateSource", expand_x=True)]
    ]

    window = sg.Window(windowTitle, layout=layout, modal=True, finalize=True, keep_on_top=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event is not None:
            if event in ['numberPages', 'studiedPages']:
                updateDeadline(window=window, values=values, studySlotsInfo=studySlotsInfo, isBook=True)

            if event == "STUDY_SLOTS":
                arrAmounts = []
                bookStudyDays = []
                for x in range(7):
                    if studyDays[x]:
                        arrAmounts.append(int(values[f"INPUT_TEXT_SESSIONS_{weekdays[x]}"]))
                        bookStudyDays.append(True)
                    else:
                        arrAmounts.append(0)
                        bookStudyDays.append(False)
                
                if sum(arrAmounts) > 0:
                    type = values['textSource']
                    studySlotsInfo = getStudySlots(type=type, studyDays=bookStudyDays, arrAmount=arrAmounts, defaults=studySlotsInfo)
                    updateDeadline(window=window, values=values, studySlotsInfo=studySlotsInfo)
                else:
                    sg.popup_ok('Insert almost one session!', title="WARNING", keep_on_top=True, modal=True)

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

                isTextSource = values['textSource']

                numberPagesStr = values['numberPages']
                studiedPagesStr = values['entryStudiedPages']

                nameBook = values['nameDeck']
                filename = values['pathSource']

                if checkStrIntInput(numberPagesStr) and checkStrIntInput(studiedPagesStr):

                    numberPages = int(numberPagesStr)
                    studiedPages = int(studiedPagesStr)


                    if not isTextSource:
                        url = window['entryStudiedPages']
                        pathVideo = window['entryStudiedPages']

                        viewedMinutes = int(window['viewedMinutes'])
                        durationMinutes = int(window['durationMinutes'])

                    if numberPages > 0 and studiedPages >= 0:
                        if studySlotsInfo is not None:
                            
                            deadline = calculateDeadline(arrSessionWeek=studySlotsInfo, totalPages=numberPages, studiedPages=studiedPages)

                            parameters = (nameBook, numberPages, studiedPages, filename, str(studySlotsInfo), deadline, datetime.now())
                            
                            if not isTextSource:
                                parameters = (nameBook, str(studySlotsInfo), deadline, url, durationMinutes, viewedMinutes)

                            if command == 'modify':
                                parameters = parameters + (sourceID, )
                                                        
                            cursor.execute(query, parameters)
                            con.commit()
                            break
                        else:
                            sg.popup_ok('You have to set your study slots!', title="WARNING", keep_on_top=True, modal=True)
                    else:
                        sg.popup_ok('Please, set the correct values!', title="WARNING", keep_on_top=True, modal=True)
                else:
                    sg.popup_ok('Please, set the correct values!', title="WARNING", keep_on_top=True, modal=True)
    
    window.close()