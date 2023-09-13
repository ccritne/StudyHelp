from functions import *
from addScheme import updateScheme

def viewScheme(flashcardID):
    if flashcardID is not None:      
        cursor.execute(f"SELECT filenameScheme FROM flashcards WHERE ID={flashcardID}")
        filename = cursor.fetchone()[0]
        
        condWindowVisible = False 

        if filename is not None:
            img = convert_to_bytes(filename, (800, 500))

            if img is None: #ERROR TO FIND THE IMAGE PROBABLY DELETED OR MOVED IT
                
                filename = updateScheme(flashcardID=flashcardID)

                if filename is not None:
                    img = convert_to_bytes(filename, (800, 500))
                    condWindowVisible = True 
            else:
                condWindowVisible = True
            
            layout = [
                        [sg.Image(data=img, key="imgScheme", size=(800, 500))],
                        [sg.HorizontalSeparator()],
                        [sg.Button('Change scheme', key="changeScheme")]
                    ]
            
            if condWindowVisible:
                window = sg.Window("PopupScheme", layout=layout, finalize=True)
            
                while True:
                    event, values = window.read()
                    if event in (sg.WIN_CLOSED, 'Exit'):
                        break
                    
                    if event is not None:
                        if event == "changeScheme":
                            filename = updateScheme(flashcardID=flashcardID)
                            img = convert_to_bytes(filename, (800, 500))
                            window['imgScheme'].update(data=img)

                window.close()
        else:
            updateScheme(flashcardID=flashcardID)
