from functions import *
from today_study import today_study_flashcards


def see_today_sessions():
    info_decks = get_info_decks()
    set_table_deck(info_decks)

    layout = [
        [
            sg.Table(
                values=info_decks,
                headings=["ID", "Name", "TODO"],
                key="info_decks",
            )
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("Start", key="start_deck")],
    ]

    window = sg.Window(
        "Table of Decks", layout=layout, keep_on_top=True, modal=True, finalize=True
    )

    while True:
        event, values = window.read()

        # START BINDING DECKSLAYOUT EVENTS
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event is not None:
            if event == "start_deck" and values["info_decks"] != []:
                played_source_id = get_table_deck()[values["info_decks"][0]][0]

                today_flashcards_of_source = get_today_flashcards_source(
                    played_source_id
                )

                set_flashcards_array(today_flashcards_of_source)

                while len(get_flashcards_array()) > 0:
                    state = today_study_flashcards()

                    window["info_decks"].update(values=get_table_deck())
                    if state == "EXIT":
                        break

        # END BINDING DECKSLAYOUT EVENTS

    window.close()
