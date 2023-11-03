import PySimpleGUI as sg
from functions import from_text_to_elements


def preview_card(text_front: str, text_back: str):
    """
    It previews the card into a new window.
    """
    # Rendering the text in LaTeX format:
    elements_front = from_text_to_elements(text_front)
    elements_back = from_text_to_elements(text_back)

    layout = [
        [sg.Text(text="Front: ")],
        [
            sg.Column(
                elements_front,
                scrollable=True,
                vertical_scroll_only=True,
                expand_x=True,
                expand_y=True,
                size=(None, 150),
                justification="center",
            )
        ],
        [sg.Text(text="Back: ")],
        [
            sg.Column(
                elements_back,
                scrollable=True,
                vertical_scroll_only=True,
                expand_x=True,
                size=(None, 150),
                justification="center",
            )
        ],
    ]

    window = sg.Window(
        "Preview Card",
        size=(500, 400),
        layout=layout,
        keep_on_top=True,
        modal=True,
        finalize=True,
        resizable=True,
    )

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

    window.close()
