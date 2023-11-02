from functions import *
from view_scheme import view_scheme


def today_study_flashcards() -> str:
    state = "OK"

    frontText: list = copy.copy(get_flashcards_array()[0][1])
    backText: list = copy.copy(get_flashcards_array()[0][2])

    set_front_layout(from_text_to_elements(frontText))
    set_back_layout(from_text_to_elements(backText))

    layout = [
        [
            sg.Text("Front: "),
            sg.Column(
                layout=get_front_layout(),
                key="frontLayout",
                scrollable=True,
                vertical_scroll_only=True,
                expand_x=True,
                expand_y=True,
                size=(None, 150),
                justification="center",
            ),
        ],
        [sg.Input(key="backTryInput")],
        [
            sg.Text("Your try: ", visible=False, key="displayTextBackTryInput"),
            sg.Text(key="textBackTryInput", visible=False),
        ],
        [
            sg.Text("Solution: ", visible=False, key="displayTextSolution"),
            sg.Column(
                layout=get_back_layout(),
                key="backLayout",
                visible=False,
                scrollable=True,
                vertical_scroll_only=True,
                expand_x=True,
                expand_y=True,
                size=(None, 150),
                justification="center",
            ),
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Button("No", key="backZero", visible=False),
            sg.Button("Yes", key="advanceBox", visible=False),
            sg.Button("Scheme", key="seeScheme", visible=False, button_color="Orange"),
        ],
        [sg.Button("Back", key="EVENT_BACK_StudyLayout")],
        [sg.Button("Solution", key="seeSolution", button_color="Green")],
        [sg.Button("Home", key="EVENT_HOME_Today")],
    ]

    window = sg.Window(
        "Flashcard", layout=layout, finalize=True, keep_on_top=True, modal=True
    )

    window["backTryInput"].bind("<Return>", "_Enter")

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            state = "EXIT"
            break

        if event is not None:
            if event == "seeScheme":
                flashcard_ID = get_flashcards_array()[0][0]
                view_scheme(flashcard_ID)

            if event in ["backTryInput_Enter", "seeSolution"]:
                window["backTryInput"].update(visible=False)
                window["displayTextBackTryInput"].update(visible=True)
                window["displayTextSolution"].update(visible=True)
                window["textBackTryInput"].update(visible=True)
                window["textBackTryInput"].update(value=values["backTryInput"])

                window["backLayout"].update(visible=True)

                window["backZero"].update(visible=True)
                window["advanceBox"].update(visible=True)
                window["seeScheme"].update(visible=True)

            if event in ["backZero", "advanceBox"]:
                flashcard_ID = get_flashcards_array()[0][0]

                new_box = 0
                deadline_str = datetime.now().strftime("%Y-%m-%d")
                if event == "advanceBox":
                    deadline_str = (
                        datetime.now()
                        + timedelta(days=pow(2, get_flashcards_array()[0][3]))
                    ).strftime("%Y-%m-%d")
                    new_box = get_flashcards_array()[0][3] + 1
                    remove_flashcard(0)
                else:
                    retry = get_flashcards_array()[0]
                    remove_flashcard(0)
                    append_flashcard(retry)

                # I update new_box after the determination of deadline because
                # the second rep is after 1 day not after 2 days.

                cursor.execute(
                    f"""UPDATE flashcards SET deadline="{deadline_str}", box={new_box} WHERE ID={flashcard_ID}"""
                )
                con.commit()

                break

    window.close()

    return state
