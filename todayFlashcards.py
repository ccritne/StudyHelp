import PySimpleGUI as sg
from functions import getInfoDecks, setTableDeck, getTableDeck
from functions import getTodayFlashcardsSource, setFlashcardsArray, getFlashcardsArray
from todayStudy import todayStudyFlashcards

def seeTodaySessions():
    infoDecks = getInfoDecks()
    setTableDeck(infoDecks)
    
    layout = [
        [sg.Table(
            values=infoDecks,
            headings=['ID', 'Name', 'TODO'],
            key="infoDecks",
        )],
        [sg.HorizontalSeparator()],
        [sg.Button("Start", key="startDeck")]
        ]

    window = sg.Window('Table of Decks', layout=layout, keep_on_top=True, modal=True, finalize=True)

    while True:

        event, values = window.read()

        ### START BINDING DECKSLAYOUT EVENTS
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event is not None:
            if event == 'startDeck':
                playedSourceID = getTableDeck()[values['infoDecks'][0]][0]

                todayFlashcardsOfSource = getTodayFlashcardsSource(playedSourceID)

                setFlashcardsArray(todayFlashcardsOfSource)
                
                while len(getFlashcardsArray()) > 0:
                    state = todayStudyFlashcards()

                    window['infoDecks'].update(values=getTableDeck())
                    if state == "EXIT":
                        break
                

        ### END BINDING DECKSLAYOUT EVENTS  

    window.close()