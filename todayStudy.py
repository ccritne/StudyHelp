import PySimpleGUI as sg
from functions import getFlashcardsArray, setFrontLayout, setBackLayout 
from functions import fromTextToElements, getFrontLayout, getBackLayout 
from functions import appendFlashcard, removeFlashcard
from setup import cursor, con
from datetime import datetime, timedelta
import copy
from viewScheme import viewScheme

def todayStudyFlashcards() -> str:

    state = "OK"

    frontText : list = copy.copy(getFlashcardsArray()[0][1])
    backText : list = copy.copy(getFlashcardsArray()[0][2])

    setFrontLayout(fromTextToElements(frontText))
    setBackLayout(fromTextToElements(backText))

    layout = [
        [sg.Text('Front: '), sg.Column(layout=getFrontLayout(), key="frontLayout", scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(None, 150), justification='center')],
        [sg.Input(key='backTryInput')],
        [sg.Text('Your try: ', visible=False, key="displayTextBackTryInput"), sg.Text(key="textBackTryInput", visible=False)],
        [sg.Text('Solution: ', visible=False, key="displayTextSolution"), sg.Column(layout=getBackLayout(), key="backLayout", visible=False, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(None, 150), justification='center')],
        [sg.HorizontalSeparator()],
        [sg.Button('No', key='backZero', visible=False), sg.Button('Yes', key='advanceBox', visible=False), sg.Button('Scheme', key='seeScheme', visible=False, button_color="Orange")],
        [sg.Button('Back', key="EVENT_BACK_StudyLayout")],
        [sg.Button('Solution', key="seeSolution", button_color="Green")],
        [sg.Button('Home', key="EVENT_HOME_Today")],

    ]

    window = sg.Window('Flashcard', layout=layout, finalize=True, keep_on_top=True, modal=True)
    
    window['backTryInput'].bind("<Return>", "_Enter")

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            state = "EXIT"
            break
        
        if event is not None:
            if event == "seeScheme":
                flashcardID = getFlashcardsArray()[0][0] 
                viewScheme(flashcardID)

            if event in ["backTryInput_Enter", "seeSolution"]:
                window['backTryInput'].update(visible=False)
                window['displayTextBackTryInput'].update(visible=True)
                window['displayTextSolution'].update(visible=True)
                window['textBackTryInput'].update(visible=True)
                window['textBackTryInput'].update(value=values['backTryInput'])

                window['backLayout'].update(visible=True)

                window['backZero'].update(visible=True)
                window['advanceBox'].update(visible=True)
                window['seeScheme'].update(visible=True)

            if event in ['backZero', 'advanceBox']:

                flashcardID = getFlashcardsArray()[0][0]

                newBox = 0 
                deadlineStr = datetime.now().strftime('%Y-%m-%d')
                if event == 'advanceBox':
                    deadlineStr = (datetime.now() + timedelta(days=pow(2, getFlashcardsArray()[0][3]))).strftime("%Y-%m-%d")
                    newBox = getFlashcardsArray()[0][3] + 1
                    removeFlashcard(0)
                else:
                    retry = getFlashcardsArray()[0]
                    removeFlashcard(0)
                    appendFlashcard(retry)
                
                # I update newBox after the determination of deadline because 
                # the second rep is after 1 day not after 2 days.

                cursor.execute(f'''UPDATE flashcards SET deadline="{deadlineStr}", box={newBox} WHERE ID={flashcardID}''')
                con.commit()
                
                break

    window.close()

    return state