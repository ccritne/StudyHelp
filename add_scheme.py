from functions import *


def save_scheme(flashcard_ID, values):
    filename = values["filenameScheme"]
    exit_message = "EXIT_SUCCESS"

    if exists_filename(filename):
        query = f"UPDATE flashcards SET filenameScheme=? WHERE ID=?"
        parameters = (filename, flashcard_ID)
        cursor.execute(query, parameters)
        con.commit()
    else:
        sg.popup_error("Path Wrong", keep_on_top=True, modal=True)
        exit_message = "PATH_WRONG"

    return exit_message


def update_scheme(flashcard_ID: int) -> (str, str):
    layout = [
        [sg.Text("Please, select a file", size=(20, 1))],
        [
            sg.InputText(key="filenameScheme"),
            sg.FileBrowse(file_types=(("Image Portable Network Graphics", "*.png"),)),
        ],
        [sg.Column([[sg.Button("Save", key="Save_scheme")]], justification="right")],
    ]

    window = sg.Window(
        layout=layout, title="File selector", keep_on_top=True, modal=True
    )

    filename: str = ""

    while True:
        event, values = window.read()

        if event in [sg.WIN_CLOSED, "Exit"]:
            filename = ""
            exit_message = "EXIT_WINDOW"
            break

        if event == "Save_scheme":
            if "EXIT_SUCCESS" == save_scheme(flashcard_ID, values):
                break

    window.close()

    return filename, exit_message