from functions import *
from viewScheme import viewScheme
from preview import previewCard
from updateSource import updateSource
from addCard import addCard
from tkinter import *

def updateFlashcardsInputs(window : sg.Window, front : str, back : str):
    if len(getFlashcardsArray())>0:
        window['flashcardInputs'].update(visible=True)
        window['frontInput'].update(value=front)
        window['backInput'].update(value=back)
    else:
        window['flashcardInputs'].update(visible=False)
        window['frontInput'].update(value="")
        window['backInput'].update(value="")

def updateSelectedSource(window : sg.Window, row : int):

    sourceID = None

    if row is not None:
        sourceID = getSourcesArray()[row][0]
        window['tableSources'].update(select_rows=[row])
    
    setSelectedSourceID(sourceID)

    updateFlashcardsTable(window)
    updateSelectedFlashcards(window, 0)

def updateFlashcardsTable(window : sg.Window):

    sourceID = getSelectedSourceID()
    
    flashcardsArr = []

    if sourceID is not None:
        flashcardsArr = getFlashcardsForTable(sourceID)
    
    setFlashcardsArray(flashcardsArr)
    
    window['tableFlashcards'].update(values=flashcardsArr)

def updateSourcesTable(window : sg.Window):

    sourcesNames = allSourcesNames()

    setSourcesArray(sourcesNames)
        
    window['tableSources'].update(values=sourcesNames)

def updateSelectedFlashcards(window : sg.Window, row : int):
    
    flashcardsArr = getFlashcardsArray()

    front = str()
    back = str()

    slFlashcardID = None
    
    if flashcardsArr != []:

        if row > len(flashcardsArr):
            row = 0
            
        slFlashcardID = flashcardsArr[row][0]
        front = flashcardsArr[row][1]
        back = flashcardsArr[row][2]
        window['tableFlashcards'].update(select_rows=[row])
        
    setSelectedFlashcardID(slFlashcardID)
    updateFlashcardsInputs(window=window, front=front, back=back)
            
def updateTables(window):

    updateSourcesTable(window)
    
    updateSelectedSource(window, 0)

    updateSelectedFlashcards(window, 0)

def browseFlashcards():

    condLayoutFlashcardsVisible = True

    sourcesNames = allSourcesNames()

    setSelectedSourceID(None)
    setRowSources(None)
    setFlashcardsArray(None)
    setSelectedFlashcardID(None)
    setRowFlashcards(None)

    if sourcesNames != []:
        firstSourceID = sourcesNames[0][0]
        setSelectedSourceID(firstSourceID)
        setRowSources(0)

        flashcardsArr = getFlashcardsForTable(firstSourceID)
        setFlashcardsArray(flashcardsArr)

        firstFlashcardID = None
        rowFlashcard = None

        if flashcardsArr != []:
            firstFlashcardID = flashcardsArr[0][0]
            rowFlashcard = 0
        else:
            condLayoutFlashcardsVisible = False
        
        setSelectedFlashcardID(firstFlashcardID)
        setRowFlashcards(rowFlashcard)

    else:
        condLayoutFlashcardsVisible = False


    setSourcesArray(sourcesNames)

    flashcardsArr = getFlashcardsArray()
    
    right_click_sources = ['Sources', ['Add source', 'Open source', 'Change file', 'Modify source', 'Delete source']]

    sourcesTable = sg.Table(
                                values=sourcesNames if sourcesNames is not None else [[]], 
                                headings=['ID', 'Name'], 
                                key="tableSources",
                                enable_click_events=True,
                                justification='l',
                                hide_vertical_scroll=True,
                                col_widths=[3, 10],
                                auto_size_columns=False,
                                expand_x=False,
                                num_rows=5,
                                row_height=40,
                                right_click_menu=right_click_sources
                                )
    
    right_click_flashcards = ['Flashcards', ['Add card', 'Delete card', 'Reschedule expired cards', 'Change box']]

    flashcardsTable = sg.Table(
                                values=flashcardsArr if flashcardsArr is not None else [[]], 
                                headings=['ID', 'Front', 'Back', 'Deadline', 'Box'], 
                                key="tableFlashcards",
                                justification='l',
                                hide_vertical_scroll=True,
                                enable_click_events=True,
                                col_widths=[3, 30, 30, 8, 3],
                                auto_size_columns=False,
                                expand_x=False,
                                num_rows=10,
                                row_height=20,
                                right_click_menu=right_click_flashcards
                            )



    menuBar = [
        ['File', 'Exit'],
        right_click_sources,
        right_click_flashcards,
        ['&Help', '&About...'],
    ]

    frontDefaultText = ""
    backDefaultText = ""
    if flashcardsArr != []: 
        frontDefaultText = flashcardsArr[0][1] 
        backDefaultText = flashcardsArr[0][2]

    flashcardInputs = [       
                            [sg.Column([[sg.Button('Latex', key='addLatex')]], justification='right')],
                            [sg.Text('Front'), sg.InputText(default_text=frontDefaultText, key='frontInput', expand_x=True, enable_events=True, size=(100, 1))],
                            [sg.Text('Back'), sg.InputText(default_text=backDefaultText, key='backInput', expand_x=True, enable_events=True, size=(100, 1))],
                            [sg.Button('Save', key="saveFlashcard"), sg.Button('View Scheme', key="viewScheme"), sg.Button('Preview', key="previewCard")],
                    ]

    layout = [
        [
            [sg.Menu(menuBar)],
            [
                sourcesTable,
                flashcardsTable
            ],
            [sg.Column(flashcardInputs, key='flashcardInputs', visible=condLayoutFlashcardsVisible)]
        ]
    ]

    window = sg.Window(title="Decks & Flashcards", layout=layout, modal=True, finalize=True)
    
    if len(sourcesNames) > 0:
        setRowSources(row=0)
        updateSelectedSource(window=window, row=0)
    if len(flashcardsArr) > 0:
        setRowFlashcards(row=0)
        updateSelectedFlashcards(window=window, row=0)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event is not None:
            ### EVENTS FOR CLICK IN TABLES

            if event[1] == '+CLICKED+' and (event[2][0] is not None and event[2][0] >=0) and getSourcesArray() is not None:
                row = event[2][0]

                match event[0]:
                    case "tableSources":
                        setRowSources(row=row)
                        updateSelectedSource(window=window, row=row)
                    case "tableFlashcards":
                        setRowFlashcards(row=row)
                        updateSelectedFlashcards(window=window, row=row)

            ###

            ### EVENTS FOR VIEWING AND LOADING SCHEME

            if event == "viewScheme":
                viewScheme(flashcardID=getSelectedFlashcardID())

            ###

            ### EVENTS FOR FLASHCARD CHANGES 

            if event in ["frontInput_Enter", "backInput_Enter", "saveFlashcard"]:
                query = "UPDATE flashcards SET front = ?, back = ? WHERE ID = ?"
                
                front = values['frontInput']
                back = values['backInput']
                flashcardID = getSelectedFlashcardID()
                
                parameters = (front, back, flashcardID)

                cursor.execute(query, parameters)
                con.commit()

                updateFlashcardsTable(window)
                updateSelectedFlashcards(window, getRowFlashcards())


            if event == 'frontInput_LClick':
                setBackInputSelected(False)
                setFrontInputSelected(True)

            if event == 'backInput_LClick':
                setFrontInputSelected(False)
                setBackInputSelected(True)

            if event == 'previewCard':
                textFront = values['frontInput']
                textBack = values['backInput']
                previewCard(textFront=textFront, textBack=textBack)

            if event == 'addLatex':
                key = None
                if getFrontInputSelected():
                    key = 'frontInput'
                    
                if getBackInputSelected():
                    key = 'backInput'
                
                if key is not None:
                    widget = window[key].Widget
                    cursor_pointer = widget.index(INSERT)
                    newText = values[key][:cursor_pointer] + "[latex][/latex]" + values[key][cursor_pointer:]
                    window[key].update(value=newText)
                    widget.icursor(cursor_pointer+7)

            ###

            ### RIGHT CLICK MENU EVENTS

            ###

            ### MENU BAR EVENTS

            ## BOOK BAR EVENTS

            if event in ["Add source", "Modify source"]:

                if event == "Add source":
                    updateSource()
                if event == "Modify source":
                    updateSource("MODIFY")

                updateTables(window=window)
                
            if event == "Delete source":
                response = sg.popup_yes_no(f'Do you want to delete the source and his content?')
                if response == 'Yes':
                    cursor.execute(f'DELETE FROM sources WHERE ID={getSelectedSourceID()}')
                    con.commit()
                    cursor.execute(f'DELETE FROM flashcards WHERE sourceID={getSelectedSourceID()}')
                    con.commit()
                    
                    updateTables(window=window)

            if event == "Open source":
                filename = cursor.execute(f'SELECT filename FROM sources where ID={getSelectedSourceID()}').fetchone()[0]
                if filename in [None, ""]:
                    filename = sg.popup_get_file('Please, select a file',  default_path="", title="File selector", file_types=(('Portable Document Format', 'PDF'),), keep_on_top=True, modal=True)
                    cursor.execute(f'UPDATE sources SET filename="{filename}" WHERE ID={getSelectedSourceID()}')
                    con.commit()
                else:
                    import webbrowser
                    webbrowser.open_new(filename)
            
            if event == "Change file":
                oldFilename = cursor.execute(f'SELECT filename FROM sources where ID={getSelectedSourceID()}').fetchone()[0]
                filename = sg.popup_get_file('Please, select a file',  default_path=oldFilename,title="File selector", file_types=(('Portable Document Format', 'PDF'),), keep_on_top=True, modal=True)
                if filename not in [None, ""]:
                    cursor.execute(f'UPDATE sources SET filename="{filename}" WHERE ID={getSelectedSourceID()}')
                    con.commit()

            ## 

            ## CARD BAR EVENTS

            if event == "Add card":
                addCard()
                updateFlashcardsTable(window)
                updateSelectedFlashcards(window, len(getFlashcardsArray()) - 1)
                window['tableFlashcards'].Widget.see(len(getFlashcardsArray()))
                if not condLayoutFlashcardsVisible:
                    condLayoutFlashcardsVisible = True
                    window['frontInput'].bind("<Return>", "_Enter")
                    window['backInput'].bind("<Return>", "_Enter")
                    window['frontInput'].bind("<Button-1>", "_LClick")
                    window['backInput'].bind("<Button-1>", "_LClick")

            
            if event == "Delete card":
                cursor.execute(f'DELETE FROM flashcards WHERE ID={getSelectedFlashcardID()}')
                con.commit()
                updateFlashcardsTable(window)
                updateSelectedFlashcards(window, 0)
                window['tableFlashcards'].Widget.see(1)


            if event == "Reschedule expired cards":
                todayStr = datetime.now().strftime('%Y-%m-%d')
                query = 'UPDATE flashcards SET deadline = ? WHERE deadline < ?'
                parameters = (todayStr, todayStr)
                cursor.execute(query, parameters)
                con.commit()
                updateFlashcardsTable(window)
                updateSelectedFlashcards(window, 0)
                window['tableFlashcards'].Widget.see(1)
            
            if event == "Change box":

                continue
            
            ##

            ###



    window.close()
