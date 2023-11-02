from functions import *
from add_scheme import update_scheme


def view_scheme(flashcard_id: int):
    if flashcard_id is not None:
        cursor.execute(
            "SELECT filenameScheme FROM flashcards WHERE id=?", (flashcard_id,)
        )

        filename = cursor.fetchone()[0]

        img = None

        cond_window_visible = True

        if exists_filename(filename):
            img = convert_to_bytes(filename, (800, 500))

        while not exists_img(img):
            filename, result = update_scheme(flashcard_id=flashcard_id)

            if result == "EXIT_WINDOW":
                cond_window_visible = False
                break

            if exists_filename(filename):
                img = convert_to_bytes(filename, (800, 500))

        if cond_window_visible:
            layout = [
                [sg.Image(data=img, key="img_scheme", size=(800, 500))],
                [sg.HorizontalSeparator()],
                [sg.Button("Change scheme", key="change_scheme")],
            ]

            window = sg.Window("PopupScheme", layout=layout, finalize=True)

            while True:
                event, values = window.read()
                if event in (sg.WIN_CLOSED, "Exit"):
                    break

                if event is not None:
                    if event == "change_scheme":
                        filename = update_scheme(flashcard_id=flashcard_id)

                        if exists_filename(filename):
                            img = convert_to_bytes(filename, (800, 500))
                            window["img_scheme"].update(data=img)
                        else:
                            sg.popup_error("Path wrong!", keep_on_top=True, modal=True)

            window.close()
