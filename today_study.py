from functions import *
from view_diagram import view_diagram


def today_study_flashcards() -> str:
    state = "OK"

    frontText: list = copy.copy(get_flashcards_list()[0][1])
    backText: list = copy.copy(get_flashcards_list()[0][2])

    set_front_layout(from_text_to_elements(frontText))
    set_back_layout(from_text_to_elements(backText))

    layout = [
        [
            sg.Text("Front: "),
            sg.Column(
                layout=get_front_layout(),
                key="front_layout",
                scrollable=True,
                vertical_scroll_only=True,
                expand_x=True,
                expand_y=True,
                size=(None, 150),
                justification="center",
            ),
        ],
        [sg.Input(key="back_try_input")],
        [
            sg.Text("Your try: ", visible=False, key="display_text_back_try_input"),
            sg.Text(key="text_back_try_input", visible=False),
        ],
        [
            sg.Text("Solution: ", visible=False, key="display_text_solution"),
            sg.Column(
                layout=get_back_layout(),
                key="back_layout",
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
            sg.Button("No", key="back_zero", visible=False),
            sg.Button("Yes", key="advance_box", visible=False),
            sg.Button(
                "diagram", key="see_diagram", visible=False, button_color="Orange"
            ),
        ],
        [sg.Button("Back", key="EVENT_BACK_study_layout")],
        [sg.Button("Solution", key="see_solution", button_color="Green")],
        [sg.Button("Home", key="EVENT_HOME_Today")],
    ]

    window = sg.Window(
        "Flashcard", layout=layout, finalize=True, keep_on_top=True, modal=True
    )

    window["back_try_input"].bind("<Return>", "_Enter")

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            state = "EXIT"
            break

        if event is not None:
            if event == "see_diagram":
                flashcard_id = get_flashcards_list()[0][0]
                view_diagram(flashcard_id)

            if event in ["back_try_input_Enter", "see_solution"]:
                window["back_try_input"].update(visible=False)
                window["display_text_back_try_input"].update(visible=True)
                window["display_text_solution"].update(visible=True)
                window["text_back_try_input"].update(visible=True)
                window["text_back_try_input"].update(value=values["back_try_input"])

                window["back_layout"].update(visible=True)

                window["back_zero"].update(visible=True)
                window["advance_box"].update(visible=True)
                window["see_diagram"].update(visible=True)

            if event in ["back_zero", "advance_box"]:
                flashcard_id = get_flashcards_list()[0][0]

                new_box = 0
                deadline_str = datetime.now().strftime("%Y-%m-%d")
                if event == "advance_box":
                    deadline_str = (
                        datetime.now()
                        + timedelta(days=pow(2, get_flashcards_list()[0][3]))
                    ).strftime("%Y-%m-%d")
                    new_box = get_flashcards_list()[0][3] + 1
                    remove_flashcard(0)
                else:
                    retry = get_flashcards_list()[0]
                    remove_flashcard(0)
                    append_flashcard(retry)

                # I update new_box after the determination of deadline because
                # the second rep is after 1 day not after 2 days.

                cursor.execute(
                    "UPDATE flashcards SET deadline=?, box=? WHERE id=?",
                    (deadline_str, new_box, flashcard_id),
                )
                con.commit()

                break

    window.close()

    return state
