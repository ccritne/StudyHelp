from functions import *
from browseFlashcards import browseFlashcards
from viewScheme import viewScheme
from todayStudy import todayStudyFlashcards

def makeMainWindow():

    MenuLayout = [
        [sg.Button('Flashcards', key="flashcards", size=225)],
        [sg.Button('Check deadlines', key="deadlines", size=225)],
        [sg.Button('Study sources', key="studySource", size=225)],
        [sg.Button('To-Do List', key="todolist", size=225)],
        [sg.Button('Settings', key="settings", size=225)],
    ]

    FlashcardsLayout = [
        [sg.Button('Browse', key="browseFlashcards", size=225)],
        [sg.Button('Study', key="studyFlashcards", size=225)],
        [sg.HorizontalSeparator()],
        [sg.Button('Menu', key="EVENT_MENU_Flashcards", size=225)]
    ]

    decksLayout = [
        [
                sg.Table(
                    values=[], 
                    headings=["ID","Source Name", "Today"],
                    enable_events=True, 
                    hide_vertical_scroll=True,
                    justification="center",
                    key="studyDeck"
            )
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Button('Back', key="EVENT_BACK_Deck"),
            sg.Button('Home', key="EVENT_MENU_Deck"),
            sg.Button('Start', key="startDecks"),
        ]
    ]



    DeadlinesLayout = [
        [
            sg.Table(
                    values=[], 
                    headings=["ID","Source Name", "Deadline"],
                    hide_vertical_scroll=True,
                    justification="center",
                    select_mode="none",
                    key="deadlinesDeck"
            )
        ],
        [sg.HorizontalSeparator()],
        [sg.Button('Menu', key="EVENT_MENU_Deadlines", size=225)]
    ]

    BooksLayout = [
        [sg.HorizontalSeparator()],
        [sg.Button('Menu', key="EVENT_MENU_Books", size=225)]
    ]
    
    studyDays = getSettingsValue('studyDays')

    SettingsLayout = [
                [sg.Text('Max study hour', size=(15, 1)), sg.Input(default_text=getSettingsValue('maxStudyHour'), key='maxStudyHour', size=(5, 1))],
                [sg.Text('Hour for Notification', size=(15, 1)), sg.Combo([x for x in range(24)], key='defaultHourNotification', default_value=getSettingsValue('defaultHourNotification'), size=(5,1))],
                [sg.Text('Days ')],
                [sg.Checkbox(text='Mon', size=(6, 1), key='monSettings', default=bool(int(studyDays[0]))), sg.Checkbox(text='Fri', size=(6, 1), key='friSettings', default=bool(int(studyDays[4])))],
                [sg.Checkbox(text='Tue', size=(6, 1), key='tueSettings', default=bool(int(studyDays[1]))), sg.Checkbox(text='Sat', size=(6, 1), key='satSettings', default=bool(int(studyDays[5])))],
                [sg.Checkbox(text='Wed', size=(6, 1), key='wedSettings', default=bool(int(studyDays[2]))), sg.Checkbox(text='Sun', size=(6, 1), key='sunSettings', default=bool(int(studyDays[6])))],
                [sg.Checkbox(text='Thu', size=(6, 1), key='thuSettings', default=bool(int(studyDays[3])))],
                [sg.HorizontalSeparator()],
                [sg.Button('Menu', key="EVENT_MENU_Settings")]
    ]
    
    dt = datetime.combine(datetime.now(), time(0, 0))
    setSelectedDate(dt)
    
    right_click_calendar = ['Edit', ['This event', 'This and all following events', 'All events']]

    def getToDoDataOf(date):
        query = f'SELECT * FROM calendar WHERE (startDate <= ?  and  ? <= endDate and weekReps = "0000000") or (startDate <= ? and substr(weekReps, strftime("%w",?), 1) = "1" and weekReps <> "0000000") ORDER BY insertedDay'
        parameters = (date, date, date, date)

        cursor.execute(query, parameters)
        result = cursor.fetchall()

        ret = []
        for x in result:
            ret.append(x[9] + "-" + x[10] + " " + x[1])

        return ret
    
    todoList = getToDoDataOf(getStringDate(getSelectedDate()))
    
    ToDoListLayout = [
                [sg.InputText(key="selectedDate", default_text=getStringDate(getSelectedDate()), size=(10, 1)), sg.Button('Select day', key='selectToDoDate')],
                [sg.Listbox(values=todoList, key="To-Do-List", no_scrollbar=True, size=(50, 18), expand_y=True, expand_x=True, right_click_menu=right_click_calendar)],
                [sg.HorizontalSeparator()],
                [sg.Button('Menu', key="EVENT_MENU_ToDoList")]
            ]
    
    menuBar = [
        ['File', 'Exit'],
        ['Help', 'About']
    ]

    layout = [
                [sg.Menu(menuBar)],
                [
                    sg.Column(MenuLayout, visible=True, key='Menu', justification="center", vertical_alignment="center"), 
                    sg.Column(FlashcardsLayout, visible=False, key="Flashcards", justification="center"), 
                    sg.Column(decksLayout, visible=False, key="Deck", justification="center"),
                    sg.Column(DeadlinesLayout, visible=False, key="Deadlines", justification="center"), 
                    sg.Column(SettingsLayout, visible=False, key="Settings", justification="center"),
                    sg.Column(BooksLayout, visible=False, key="Books", justification="center"),
                    sg.Column(ToDoListLayout, visible=False, key="ToDoList")
                ]
            ]
    
    window =  sg.Window(title="StudyHelp", layout=layout, size=(300, 400), finalize=True)
    
    window['selectedDate'].bind("<Return>", "_Enter")


    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event is not None:
            ### START BINDING MENULAYOUT EVENTS
            if event == "flashcards":
                FromTo('Menu', 'Flashcards', window)
    
            if event == "deadlines":
                books = cursor.execute('SELECT ID, name, deadline FROM sources').fetchall()
                window['deadlinesDeck'].update(values=books)
                FromTo('Menu', 'Deadlines', window)

            if event == "settings":
                FromTo('Menu', 'Settings', window)

            if event == "books":
                FromTo('Menu', 'Books', window)
            
            if event == "todolist":
                FromTo('Menu', 'ToDoList', window)

            ### END BINDING MENULAYOUT EVENTS

            ### START BINDING FLASHCARDSLAYOUT EVENTS
            
            if event == "studyFlashcards":
                setTableDeck(getInfoDecks())
                window['studyDeck'].update(values=getTableDeck())

                FromTo('Flashcards', 'Deck', window)

            ### END BINDING FLASHCARDSLAYOUT EVENTS

            ### START BINDING DECKSLAYOUT EVENTS

            if event == 'startDecks':
                playedSourceID = getTableDeck()[values['studyDeck'][0]][0]
                setFlashcardsArray(getTodayFlashcardsSource(playedSourceID))

                while len(getFlashcardsArray()) > 0:
                    state = todayStudyFlashcards()
                    if state == "EXIT":
                        break

            ### END BINDING DECKSLAYOUT EVENTS

            ### EVENTS BACK BUTTONS

            if "EVENT_BACK" in event:
                if event == "EVENT_BACK_StudyLayout":
                    tableDeck = getInfoDecks()
                    window['studyDeck'].update(values=tableDeck)
                FromTo(getActualPage(), getPreviousPage(), window)
            
            ###

            ### EVENTS FOR BROWSING FLASHCARDS AND DECKS

            if event == "browseFlashcards":
                browseFlashcards()

            ###

            

            ### MENU BUTTONS EVENT

            if "EVENT_MENU" in event:

                if "Settings" in event:
                    maxStudyHour = int(values['maxStudyHour'])
                    defaultHourNotification = int(values['defaultHourNotification'])

                    studyDays = "".join([str(int(window['monSettings'].get())),
                                        str(int(window['tueSettings'].get())),
                                        str(int(window['wedSettings'].get())),
                                        str(int(window['thuSettings'].get())),
                                        str(int(window['friSettings'].get())),
                                        str(int(window['satSettings'].get())),
                                        str(int(window['sunSettings'].get()))])
                    query = '''UPDATE settings SET  maxStudyHour= ? , 
                                                    defaultHourNotification = ?, 
                                                    studyDays = ?'''

                    parameters = (maxStudyHour, defaultHourNotification, studyDays) 

                    cursor.execute(query, parameters)
                    con.commit()
                
                
                FromTo(getActualPage(), 'Menu', window)
            ###

            ### SCHEME EVENTS

            if event == "seeScheme":
                viewScheme(flashcardID=getPlayedFlashcardID())
            
            ###

            ### TO-DO LIST EVENTS

            if event in ["selectToDoDate", 'selectedDate_Enter']:
                sDate = values['selectedDate']
                if event == 'selectToDoDate':
                    dtMon = datetime.now().month
                    selectedDate = sg.popup_get_date(close_when_chosen=True, start_mon=dtMon, no_titlebar=False, modal=True, keep_on_top=True)
                    sDate = datetime(year=selectedDate[2], month=selectedDate[0], day=selectedDate[1])
                    setSelectedDate(sDate)
                else:
                    setSelectedDate(datetime.strptime(sDate, '%Y-%m-%d'))
    
                window['selectedDate'].update(value=getStringDate(getSelectedDate()))
                window['To-Do-List'].update(values=getToDoDataOf(getSelectedDate()))

            ###
   
    window.close()
