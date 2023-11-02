from functions import *
from view_scheme import view_scheme
from preview import preview_card
from update_source import update_source
from add_card import add_card


def update_flashcards_inputs(window: sg.Window, front: str, back: str):
    if len(get_flashcards_array()) > 0:
        window["flashcard_inputs"].update(visible=True)
        window["front"].update(value=front)
        window["back"].update(value=back)
    else:
        window["flashcard_inputs"].update(visible=False)
        window["front"].update(value="")
        window["back"].update(value="")


def update_selected_source(window: sg.Window, row: int):
    source_ID = None
    sources_arr = get_sources_array()

    if row is not None and sources_arr != []:
        source_ID = sources_arr[row][0]
        window["tableSources"].update(select_rows=[row])

    set_selected_source_ID(source_ID)

    update_flashcards_table(window)
    update_selected_flashcards(window, 0)


def update_flashcards_table(window: sg.Window):
    source_ID = get_selected_source_ID()

    flashcards_arr = []

    if source_ID is not None:
        flashcards_arr = get_flashcards_for_table(source_ID)

    set_flashcards_array(flashcards_arr)

    window["tableFlashcards"].update(values=flashcards_arr)


def update_sources_table(window: sg.Window):
    sources_names = all_sources_names()

    set_sources_array(sources_names)

    window["tableSources"].update(values=sources_names)


def update_selected_flashcards(window: sg.Window, row: int):
    flashcards_arr = get_flashcards_array()

    front = str()
    back = str()

    sl_flashcard_ID = None

    if flashcards_arr != []:
        if row > len(flashcards_arr):
            row = 0

        sl_flashcard_ID = flashcards_arr[row][0]
        front = flashcards_arr[row][1]
        back = flashcards_arr[row][2]
        window["tableFlashcards"].update(select_rows=[row])

    set_selected_flashcard_ID(sl_flashcard_ID)
    update_flashcards_inputs(window=window, front=front, back=back)


def update_tables(window):
    update_sources_table(window)

    update_selected_source(window, 0)

    update_selected_flashcards(window, 0)


def browse_flashcards():
    cond_layout_flashcards_visible = True

    sources_names = all_sources_names()

    set_selected_source_ID(None)
    set_row_sources(None)
    set_selected_flashcard_ID(None)
    set_row_flashcards(None)

    set_flashcards_array([])

    if sources_names != []:
        first_source_ID = sources_names[0][0]
        set_selected_source_ID(first_source_ID)
        set_row_sources(0)

        flashcards_arr = get_flashcards_for_table(first_source_ID)
        set_flashcards_array(flashcards_arr)

        first_flashcard_ID = None
        row_flashcard = None

        if flashcards_arr != []:
            first_flashcard_ID = flashcards_arr[0][0]
            row_flashcard = 0
        else:
            cond_layout_flashcards_visible = False

        set_selected_flashcard_ID(first_flashcard_ID)
        set_row_flashcards(row_flashcard)

    else:
        cond_layout_flashcards_visible = False

    set_sources_array(sources_names)

    flashcards_arr = get_flashcards_array()

    right_click_sources = [
        "Sources",
        ["Add source", "Open source", "Change file", "Modify source", "Delete source"],
    ]

    sources_table = sg.Table(
        values=sources_names if sources_names is not None else [[]],
        headings=["ID", "Name"],
        key="tableSources",
        enable_click_events=True,
        justification="l",
        hide_vertical_scroll=True,
        col_widths=[3, 10],
        auto_size_columns=False,
        expand_x=False,
        num_rows=5,
        row_height=40,
        right_click_menu=right_click_sources,
    )

    right_click_flashcards = [
        "Flashcards",
        ["Add card", "Delete card", "Reschedule expired cards"],
    ]

    flashcards_table = sg.Table(
        values=flashcards_arr if flashcards_arr is not None else [[]],
        headings=["ID", "Front", "Back", "Deadline", "Box"],
        key="tableFlashcards",
        justification="l",
        hide_vertical_scroll=True,
        enable_click_events=True,
        col_widths=[3, 30, 30, 8, 3],
        auto_size_columns=False,
        expand_x=False,
        num_rows=10,
        row_height=20,
        right_click_menu=right_click_flashcards,
    )

    menu_bar = [
        ["File", "Exit"],
        right_click_sources,
        right_click_flashcards,
        ["&Help", "&About..."],
    ]

    front_default_text = ""
    back_default_text = ""

    if flashcards_arr != []:
        front_default_text = flashcards_arr[0][1]
        back_default_text = flashcards_arr[0][2]

    flashcard_inputs = [
        [sg.Column([[sg.Button("Latex", key="addLatex")]], justification="right")],
        [
            sg.Text("Front"),
            sg.InputText(
                default_text=front_default_text,
                key="front",
                expand_x=True,
                enable_events=True,
                size=(100, 1),
            ),
        ],
        [
            sg.Text("Back"),
            sg.Multiline(
                default_text=back_default_text,
                key="back",
                expand_x=True,
                enable_events=True,
                size=(100, 8),
            ),
        ],
        [
            sg.Button("Save", key="saveFlashcard"),
            sg.Button("View Scheme", key="viewScheme"),
            sg.Button("Preview", key="preview_card"),
        ],
    ]

    layout = [
        [
            [sg.Menu(menu_bar)],
            [sources_table, flashcards_table],
            [
                sg.Column(
                    flashcard_inputs,
                    key="flashcard_inputs",
                    visible=cond_layout_flashcards_visible,
                )
            ],
        ]
    ]

    window = sg.Window(
        title="Decks & Flashcards", layout=layout, modal=True, finalize=True
    )
    window["front"].bind("<Return>", "_Enter")
    window["back"].bind("<Return>", "_Enter")
    window["front"].bind("<Button-1>", "_LClick")
    window["front"].bind("<Tab>", "_Tab")
    window["back"].bind("<Button-1>", "_LClick")

    if len(sources_names) > 0:
        set_row_sources(row=0)
        update_selected_source(window=window, row=0)
    if len(flashcards_arr) > 0:
        set_row_flashcards(row=0)
        update_selected_flashcards(window=window, row=0)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event is not None:
            ### EVENTS FOR CLICK IN TABLES

            if (
                event[1] == "+CLICKED+"
                and (event[2][0] is not None and event[2][0] >= 0)
                and get_sources_array() is not None
            ):
                row = event[2][0]

                match event[0]:
                    case "tableSources":
                        set_row_sources(row=row)
                        update_selected_source(window=window, row=row)
                    case "tableFlashcards":
                        set_front_input_selected(False)
                        set_back_input_selected(False)
                        set_row_flashcards(row=row)
                        update_selected_flashcards(window=window, row=row)

            ###

            ### EVENTS FOR VIEWING AND LOADING SCHEME

            if event == "viewScheme":
                view_scheme(flashcard_ID=get_selected_flashcard_ID())

            ###

            ### EVENTS FOR FLASHCARD CHANGES

            if event in ["front_Enter", "back_Enter", "saveFlashcard"]:
                update_flashcard(
                    flashcard_ID=get_selected_flashcard_ID(),
                    front=values["front"],
                    back=values["back"],
                )
                update_flashcards_table(window)
                update_selected_flashcards(window, get_row_flashcards())

            check_input_click(event)

            if event == "addLatex":
                add_latex_to_input_field(window)

            if event == "preview_card":
                preview_card(text_front=values["front"], text_back=values["back"])

            ###

            ### RIGHT CLICK MENU EVENTS

            ###

            ### MENU BAR EVENTS

            ## BOOK BAR EVENTS

            if event in ["Add source", "Modify source"]:
                if event == "Add source":
                    update_source("NEW")
                if event == "Modify source":
                    update_source("MODIFY")

                update_tables(window=window)

            if event == "Delete source":
                response = sg.popup_yes_no(
                    f"Do you want to delete the source and his content?"
                )
                if response == "Yes":
                    cursor.execute(
                        f"DELETE FROM sources WHERE ID={get_selected_source_ID()}"
                    )
                    con.commit()
                    cursor.execute(
                        f"DELETE FROM flashcards WHERE source_ID={get_selected_source_ID()}"
                    )
                    con.commit()

                    update_tables(window=window)

            if event == "Open source":
                filename = cursor.execute(
                    f"SELECT filename FROM sources where ID={get_selected_source_ID()}"
                ).fetchone()[0]
                if filename in [None, ""]:
                    filename = sg.popup_get_file(
                        "Please, select a file",
                        default_path="",
                        title="File selector",
                        file_types=(("Portable Document Format", "PDF"),),
                        keep_on_top=True,
                        modal=True,
                    )
                    cursor.execute(
                        f'UPDATE sources SET filename="{filename}" WHERE ID={get_selected_source_ID()}'
                    )
                    con.commit()
                else:
                    import webbrowser

                    webbrowser.open_new(filename)

            if event == "Change file":
                old_filename = cursor.execute(
                    f"SELECT filename FROM sources where ID={get_selected_source_ID()}"
                ).fetchone()[0]
                filename = sg.popup_get_file(
                    "Please, select a file",
                    default_path=old_filename,
                    title="File selector",
                    file_types=(("Portable Document Format", "PDF"),),
                    keep_on_top=True,
                    modal=True,
                )
                if filename not in [None, ""]:
                    cursor.execute(
                        f'UPDATE sources SET filename="{filename}" WHERE ID={get_selected_source_ID()}'
                    )
                    con.commit()

            ##

            ## CARD BAR EVENTS

            if event == "Add card":
                add_card()
                update_flashcards_table(window)
                update_selected_flashcards(window, len(get_flashcards_array()) - 1)
                window["tableFlashcards"].Widget.see(len(get_flashcards_array()))
                if not cond_layout_flashcards_visible:
                    cond_layout_flashcards_visible = True

            if event == "Delete card":
                cursor.execute(
                    f"DELETE FROM flashcards WHERE ID={get_selected_flashcard_ID()}"
                )
                con.commit()
                update_flashcards_table(window)
                update_selected_flashcards(window, 0)
                window["tableFlashcards"].Widget.see(1)

            if event == "Reschedule expired cards":
                today_str = datetime.now().strftime("%Y-%m-%d")
                query = "UPDATE flashcards SET deadline = ? WHERE deadline < ?"
                parameters = (today_str, today_str)
                cursor.execute(query, parameters)
                con.commit()
                update_flashcards_table(window)
                update_selected_flashcards(window, 0)
                window["tableFlashcards"].Widget.see(1)

            ##

            ###

    window.close()
