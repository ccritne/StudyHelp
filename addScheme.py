from functions import *

def changeScheme(flashcardID):
    filename = sg.popup_get_file('Please, select a file', title="File selector", file_types=(('Image Portable Network Graphics', 'png'),), keep_on_top=True, modal=True)
    if filename is not None:
        cursor.execute(f'UPDATE flashcards SET filenameScheme="{filename}" WHERE ID={flashcardID}')
        con.commit()
        return convert_to_bytes(filename)
    
def addScheme(flashcardID):
    filename = sg.popup_get_file('Please, select a file', title="File selector", file_types=(('Image Portable Network Graphics', 'png'),), keep_on_top=True, modal=True)
    if filename is not None:
        cursor.execute(f'UPDATE flashcards SET filenameScheme="{filename}" WHERE ID={flashcardID}')
        con.commit()
        return filename