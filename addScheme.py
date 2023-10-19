from functions import *
    
def updateScheme(flashcardID : int) -> (str, str):

    layout = [
        [sg.Text('Please, select a file', size=(20,1))],
        [sg.InputText(key="filenameScheme"), sg.FileBrowse(file_types=(('Image Portable Network Graphics', '*.png'),))],
        [sg.Column([[sg.Button('Save', key='SaveScheme')]], justification='right')]
    ]

    window = sg.Window(layout=layout, title="File selector", keep_on_top=True, modal=True)
    
    filename : str = ""

    while True:
        event, values = window.read()
        
        if event in [sg.WIN_CLOSED, 'Exit']:
            filename = ""
            exitMessage = 'EXIT_WINDOW'
            break

        if event == ['SaveScheme']:
            filename = values['filenameScheme']
            if existsFilename(filename):
                query = f'UPDATE flashcards SET filenameScheme=? WHERE ID=?'
                parameters = (filename, flashcardID)
                cursor.execute(query, parameters)
                con.commit()
                exitMessage = 'SUCCESS'
                break
            else:
                sg.popup_error('Path Wrong', keep_on_top=True, modal=True)
                
    window.close()        
    
    return filename, exitMessage
            