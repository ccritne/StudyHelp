from functions import *
    
def updateScheme(flashcardID : int) -> str:

    layout = [
        [sg.Text('Please, select a file', size=(20,1))],
        [sg.InputText(key="filenameScheme"), sg.FileBrowse(file_types=(('Image Portable Network Graphics', '*.png'),))],
        [sg.Column([[sg.Button('Save', key='SaveScheme')]], justification='right')]
    ]

    window = sg.Window(layout=layout, title="File selector", keep_on_top=True, modal=True)
    
    filename = None

    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit', 'SaveScheme'):
            filename = values['filenameScheme']
            if filename is not None:
                cursor.execute(f'UPDATE flashcards SET filenameScheme="{filename}" WHERE ID={flashcardID}')
                con.commit()
            break
        
    window.close()
    
    return filename