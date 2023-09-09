from functions import *
from addScheme import *

def viewScheme(flashcardID):
    if flashcardID is not None:      
        cursor.execute(f"SELECT filenameScheme FROM flashcards WHERE ID={flashcardID}")
        filename = cursor.fetchone()[0]
        if filename is not None:
            img = convert_to_bytes(filename, (800, 500))

            layout = [
                [sg.Image(data=img, key="imgScheme", size=(800, 500))],
                [sg.HorizontalSeparator()],
                [sg.Button('Change scheme', key="changeScheme")]
            ]

            window = sg.Window("PopupScheme", layout=layout, keep_on_top=True, modal=True, finalize=True)

            while True:
                event, values = window.read()
                if event in (sg.WIN_CLOSED, 'Exit'):
                    break
                
                if event is not None:
                    if event == "changeScheme":
                        img = changeScheme(flashcardID=flashcardID)
                        window['imgScheme'].update(data=img)

            window.close()
        else:
            addScheme(flashcardID=flashcardID)
