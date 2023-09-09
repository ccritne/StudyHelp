from functions import *
from viewScheme import viewScheme
from preview import previewCard
from updateSource import updateSource
from addCard import addCard
from tkinter import *

def updateFlashcardsInputs(window, front, back):
    window['frontInput'].update(value=front)
    window['backInput'].update(value=back)

def updateSelectedSource(window, row):
    setRowSources(row)
    setSelectedSourceID(getSourcesArray()[row][0])
    window['tableSources'].update(select_rows=[row])
    updateFlashcardsTable(window)
    updateSelectedFlashcards(window, 0)
        
def updateFlashcardsTable(window):
    setFlashcardsArray(getFlashcards(getSelectedBookID()))
    window['tableFlashcards'].update(values=getFlashcardsArray())

def updateSourcesTable(window):
    setSourcesArray(allSourcesNames())
    window['tableSources'].update(values=getSourcesArray())

def updateSelectedFlashcards(window, row):
    length = len(getFlashcardsArray())

    setRowFlashcards(None)
    setSelectedFlashcardID(None)
    updateFlashcardsInputs(window=window, front="", back="")

    if length > 0:
        newRow = row
        if row > length and row is not None:
            newRow = 0
            
        setRowFlashcards(newRow)
        setSelectedFlashcardID(getFlashcardsArray()[newRow][0])
        window['tableFlashcards'].update(select_rows=[newRow])
        updateFlashcardsInputs(window=window, front=getFlashcardsArray()[newRow][1], back=getFlashcardsArray()[newRow][2])
            
def updateTables(window):

    updateSourcesTable(window)
    setSourcesArray(allSourcesNames())
    updateSelectedSource(window, 0)

    setFlashcardsArray(getFlashcards(getSelectedBookID()))    

    setSelectedFlashcardID(None)
    if len(getFlashcardsArray()) > 0:
        updateSelectedFlashcards(window, 0)

def browseFlashcards():

    setSourcesArray(allSourcesNames())
    setSelectedSourceID(getSourcesArray()[0][0])

    setFlashcardsArray(getFlashcards(getSelectedBookID()))    
    setSelectedFlashcardID(getFlashcardsArray()[0][0])

    right_click_sources = ['Sources', ['Add source', 'Open source', 'Change file', 'Modify source', 'Delete source']]

    booksTable = sg.Table(
                                values=getSourcesArray(), 
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
                                values=getFlashcardsArray(), 
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

    layout = [
        [
            [sg.Menu(menuBar)],
            [
                booksTable,
                flashcardsTable
            ],
            [
                [sg.Column([[sg.Button('Latex', key='addLatex')]], justification='right')],
                [sg.Text('Front'), sg.InputText(default_text=getFlashcardsArray()[0][1], key='frontInput', expand_x=True, enable_events=True)],
                [sg.Text('Back'), sg.InputText(default_text=getFlashcardsArray()[0][2], key='backInput', expand_x=True, enable_events=True)],
                [sg.Button('Save', key="saveFlashcard"), sg.Button('View Scheme', key="viewScheme"), sg.Button('Preview', key="previewCard")],
            ]
        ]
    ]

    window = sg.Window(title="Decks & Flashcards", layout=layout, modal=True, finalize=True)

    window['frontInput'].bind("<Return>", "_Enter")
    window['backInput'].bind("<Return>", "_Enter")
    window['frontInput'].bind("<Button-1>", "_LClick")
    window['backInput'].bind("<Button-1>", "_LClick")

    window['tableSources'].update(select_rows=[0])
    window['tableFlashcards'].update(select_rows=[0])

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event is not None:
            ### EVENTS FOR CLICK IN TABLES

            if event[1] == '+CLICKED+' and (event[2][0] is not None and event[2][0] >=0):
                row = event[2][0]

                match event[0]:
                    case "tableSources":
                        updateSelectedSource(window=window, row=row)
                    case "tableFlashcards":
                        updateSelectedFlashcards(window=window, row=row)

            ###

            ### EVENTS FOR VIEWING AND LOADING SCHEME

            if event == "viewScheme":
                viewScheme(flashcardID=getSelectedFlashcardID())

            ###

            ### EVENTS FOR FLASHCARD CHANGES 

            if event in ["frontInput_Enter", "backInput_Enter", "saveFlashcard"]:
                cursor.execute(f'''UPDATE flashcards SET front="{values['frontInput']}", back="{values['backInput']}", box=0, deadline="{datetime.now().strftime('%Y-%m-%d')}" WHERE ID={getSelectedFlashcardID()}''')
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
                    updateSource("modify", getSelectedBookID())

                updateTables(window=window)
                
            if event == "Delete source":
                response = sg.popup_yes_no(f'Do you want to delete the source and his content?')
                if response == 'Yes':
                    cursor.execute(f'DELETE FROM sources WHERE ID={getSelectedBookID()}')
                    con.commit()
                    cursor.execute(f'DELETE FROM flashcards WHERE bookID={getSelectedBookID()}')
                    con.commit()
                    
                    updateTables(window=window)

            if event == "Open source":
                filename = cursor.execute(f'SELECT filename FROM books where ID={getSelectedBookID()}').fetchone()[0]
                if filename is not None:
                    import webbrowser
                    webbrowser.open_new(filename)
                else:
                    filename = sg.popup_get_file('Please, select a file',  default_path="", title="File selector", file_types=(('Portable Document Format', 'PDF'),), keep_on_top=True, modal=True)
                    cursor.execute(f'UPDATE books SET filename="{filename}" WHERE ID={getSelectedBookID()}')
                    con.commit()
            
            if event == "Change file":
                oldFilename = cursor.execute(f'SELECT filename FROM books where ID={getSelectedBookID()}').fetchone()[0]
                filename = sg.popup_get_file('Please, select a file',  default_path=oldFilename,title="File selector", file_types=(('Portable Document Format', 'PDF'),), keep_on_top=True, modal=True)
                if filename is not None:
                    cursor.execute(f'UPDATE books SET filename="{filename}" WHERE ID={getSelectedBookID()}')
                    con.commit()

            ## 

            ## CARD BAR EVENTS

            if event == "Add card":
                addCard()
                updateFlashcardsTable(window)
                updateSelectedFlashcards(window, len(getFlashcardsArray()) - 1)
            
            if event == "Delete card":
                cursor.execute(f'DELETE FROM flashcards WHERE ID={getSelectedFlashcardID()}')
                con.commit()
                updateFlashcardsTable(window)
                updateSelectedFlashcards(window, 0)


            if event == "Reschedule expired cards":
                todayStr = datetime.now().strftime('%Y-%m-%d')
                query = 'UPDATE flashcards SET deadline = ? WHERE deadline < ?'
                parameters = (todayStr, todayStr)
                cursor.execute(query, parameters)
                con.commit()
                updateFlashcardsTable(window)
                updateSelectedFlashcards(window, 0)
            
            if event == "Change box":

                continue
            
            ##

            ###



    window.close()
