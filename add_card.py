from functions import *


def add_card():
    layout = [
        [
            [sg.Column([[sg.Button("Latex", key="addLatex")]], justification="right")],
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
                sg.Button("Save", key="saveNewFlashcard"),
                sg.Button("Preview", key="previewNewCard"),
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

            if event == "addLatex":
                add_latex_to_input_field(window)

            if event == "saveNewFlashcard":
                save_new_flashcard(
                    front=values["front"],
                    back=values["back"],
                    filename=values["filename"],
                )
                break

    window.close()
