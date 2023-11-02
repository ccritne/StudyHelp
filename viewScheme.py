import PySimpleGUI as sg
from functions import existsFilename, convert_to_bytes, existsImg
from setup import cursor
from addScheme import updateScheme


def viewScheme(flashcardID: int):
    if flashcardID is not None:
        cursor.execute(
            "SELECT filenameScheme FROM flashcards WHERE ID=?", (flashcardID,)
        )

        filename = cursor.fetchone()[0]

        img = None

        condWindowVisible = True

        if existsFilename(filename):
            img = convert_to_bytes(filename, (800, 500))

        while not existsImg(img):
            filename, result = updateScheme(flashcardID=flashcardID)

            if result == "EXIT_WINDOW":
                condWindowVisible = False
                break

            if existsFilename(filename):
                img = convert_to_bytes(filename, (800, 500))

        if condWindowVisible:
            layout = [
                [sg.Image(data=img, key="imgScheme", size=(800, 500))],
                [sg.HorizontalSeparator()],
                [sg.Button("Change scheme", key="changeScheme")],
            ]

            window = sg.Window(
                "PopupScheme", layout=layout, keep_on_top=True, finalize=True
            )

            while True:
                event, values = window.read()
                if event in (sg.WIN_CLOSED, "Exit"):
                    break

                if event is not None:
                    if event == "changeScheme":
                        filename = updateScheme(flashcardID=flashcardID)

                        if existsFilename(filename):
                            img = convert_to_bytes(filename, (800, 500))
                            window["imgScheme"].update(data=img)
                        else:
                            sg.popup_error("Path wrong!", keep_on_top=True, modal=True)

            window.close()
