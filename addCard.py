from functions import *
from tkinter import *

def addCard():

    layout = [
                [
                    [sg.Column([[sg.Button('Latex', key='addLatex')]], justification='right')],
                    [sg.Text('Front', size=(10,1)), sg.InputText(key='frontInput', expand_x=True, enable_events=True)],
                    [sg.Text('Back', size=(10,1)), sg.InputText(key='backInput', expand_x=True, enable_events=True)],
                    [sg.Text('Document', size=(10,1)), sg.InputText(key="filenameScheme"), sg.FileBrowse(file_types=(('Image Portable Network Graphics', 'png'),))],
                    [sg.Button('Save', key="saveNewFlashcard"), sg.Button('Preview', key="previewNewCard")],
                ]
            ]
    
    window = sg.Window("Add new card", layout=layout, modal=True, finalize=True, keep_on_top=True)
    window['frontInput'].bind("<Button-1>", "_LClick")
    window['backInput'].bind("<Button-1>", "_LClick")

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event is not None:

            if event == 'frontInput_LClick':
                setBackInputSelected(False)
                setFrontInputSelected(True)

            if event == 'backInput_LClick':
                setFrontInputSelected(False)
                setBackInputSelected(True)

            if event == "addLatex":
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

            if event == "saveNewFlashcard":
                textFront = values['frontInput'] 
                textBack = values['backInput'] 
                box = 0
                deadline = datetime.now().strftime('%Y-%m-%d')
                sourceID = getSelectedSourceID()
                filenameScheme = values['filenameScheme']

                query = "INSERT INTO flashcards(front, back, box, deadline, sourceID, filenameScheme) VALUES (?, ?, ?, ?, ?, ?)"

                parameters = (textFront, textBack, box, deadline, sourceID, filenameScheme)

                cursor.execute(query, parameters)
                con.commit()
                break

    window.close()