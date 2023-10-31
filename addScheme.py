import PySimpleGUI as sg
from functions import saveScheme

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

        if event == 'SaveScheme':
            if 'EXIT_SUCCESS' == saveScheme(flashcardID, values):
                break
            
                
    window.close()        
    
    return filename, exitMessage
            