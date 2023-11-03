from functions import *
from preview import preview_card
from datetime import datetime as dt
import logging

# Create log for this script:
logging.basicConfig(
    filename="logs/add_card.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)


def add_card():
    #
    # ?[Open][@ccritne][wait-answer] QUESTION:
    # Why have you inserted here this line?
    # I can avoid the insert of the card if
    # I close the window but the log will
    # say that a new card it's added.

    # Logging:
    logging.info(f"{dt.now}: Card added.")

    layout = [
        [
            [sg.Column([[sg.Button("Latex", key="add_latex")]], justification="right")],
            [
                sg.Text("Front", size=(10, 1)),
                sg.InputText(key="front", expand_x=True, enable_events=True),
            ],
            [
                sg.Text("Back", size=(10, 1)),
                sg.Multiline(
                    key="back", expand_x=True, enable_events=True, size=(100, 8)
                ),
            ],
            [
                sg.Text("Document", size=(10, 1)),
                sg.InputText(key="filename"),
                sg.FileBrowse(file_types=(("Image Portable Network Graphics", "png"),)),
            ],
            [
                sg.Button("Save", key="save_new_flashcard"),
                sg.Button("Preview", key="preview_new_card"),
            ],
        ]
    ]

    window = sg.Window(
        "Add new card", layout=layout, modal=True, finalize=True, keep_on_top=True
    )
    window["front"].bind("<Button-1>", "_LClick")
    window["front"].bind("<Tab>", "_Tab")
    window["back"].bind("<Button-1>", "_LClick")

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event is not None:
            check_input_click(event)

            if event == "add_latex":
                add_latex_to_input_field(window)

            if event == "save_new_flashcard":
                save_new_flashcard(
                    front=values["front"],
                    back=values["back"],
                    filename=values["filename"],
                )
                break
            if event == "preview_new_flashcard":
                preview_card(front=values["front"], back=values["back"])
                break

    window.close()
