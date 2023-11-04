from functions import *
from view_diagram import view_diagram
from preview import preview_card
from update_source import update_source
from add_card import add_card


def update_flashcards_inputs(window: sg.Window, front: str, back: str):
    """
    It updates the text of the flashcards inside the InputText.
    """

    visible_flashcards_inputs = False
    if len(get_flashcards_list()) > 0:
        visible_flashcards_inputs = True

    window["flashcard_inputs"].update(visible=visible_flashcards_inputs)
    window["front"].update(value=front)
    window["back"].update(value=back)


def update_selected_source(window: sg.Window, row: int):
    """
    It highlights the selected source.
    """

    source_id = None
    sources_arr = get_sources_list()

    if row is not None and sources_arr != []:
        source_id = sources_arr[row][0]
        window["table_sources"].update(select_rows=[row])
        set_row_sources(row=row)

    set_selected_source_id(source_id)

    update_flashcards_table(window)
    update_selected_flashcards(window, 0)


def update_flashcards_table(window: sg.Window):
    """
    It changes the values of flashcards table with the flashcards
    of the selected source.
    """
    source_id = get_selected_source_id()

    flashcards_arr = []

    if source_id is not None:
        flashcards_arr = get_flashcards_for_table(source_id)

    set_flashcards_list(flashcards_arr)

    window["table_flashcards"].update(values=flashcards_arr)


def update_sources_table(window: sg.Window):
    sources_names = all_sources_names()

    set_sources_list(sources_names)

    window["table_sources"].update(values=sources_names)


def update_selected_flashcards(window: sg.Window, row: int):
    """
    It highlights the selected flashcard.
    """
    flashcards_arr = get_flashcards_list()

    front = str()
    back = str()

    sl_flashcard_id = None

    if flashcards_arr != []:
        if row > len(flashcards_arr) and row <= 1:
            row = 0

        sl_flashcard_id = flashcards_arr[row][0]
        front = flashcards_arr[row][1]
        back = flashcards_arr[row][2]
        window["table_flashcards"].update(select_rows=[row])
        set_row_flashcards(row=row)

    set_selected_flashcard_id(sl_flashcard_id)
    update_flashcards_inputs(window=window, front=front, back=back)


def update_tables(window):
    update_sources_table(window)

    update_selected_source(window, 0)

    update_selected_flashcards(window, 0)


def browse_flashcards():
    """
    It shows all decks and all the flashcards of selected deck.
    """
    # If there are flashcards to display I will display it
    cond_layout_flashcards_visible = True

    sources_names = all_sources_names()  # List of dicts with IDs and names

    # Initial values for selected_source_id, row_sources, selected_flashcard_id, row_flashcards
    set_selected_source_id(None)
    set_row_sources(None)
    set_selected_flashcard_id(None)
    set_row_flashcards(None)

    set_flashcards_list([])

    if sources_names != []:
        # Exists almost one source

        # To default I set the first source as selected
        first_source_id = sources_names[0][0]
        set_selected_source_id(first_source_id)
        set_row_sources(0)

        flashcards_arr = get_flashcards_for_table(
            first_source_id
        )  # Gets the flashcards of the first source
        set_flashcards_list(flashcards_arr)

        # To default I set the next values to None because
        # it's not guaranteed the existence of flashcards
        first_flashcard_id = None
        row_flashcard = None

        if flashcards_arr != []:
            # To default if the list of flashcards is not void
            # I set the first flashcard as selected
            first_flashcard_id = flashcards_arr[0][0]
            row_flashcard = 0
        else:
            cond_layout_flashcards_visible = False

        set_selected_flashcard_id(first_flashcard_id)
        set_row_flashcards(row_flashcard)

    else:
        cond_layout_flashcards_visible = False

    set_sources_list(sources_names)

    right_click_sources = [
        "Sources",
        ["Add source", "Open source", "Change file", "Modify source", "Delete source"],
    ]

    values_table_sources = [[]]
    if sources_names is not None:
        values_table_sources = sources_names

    sources_table = sg.Table(
        values=values_table_sources,
        headings=["ID", "Name"],
        key="table_sources",
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

    values_table_flashcards = [[]]
    if get_flashcards_list() is not None:
        values_table_flashcards = get_flashcards_list()

    flashcards_table = sg.Table(
        values=values_table_flashcards,
        headings=["id", "Front", "Back", "Deadline", "Box"],
        key="table_flashcards",
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

    if get_flashcards_list() != []:
        front_default_text = flashcards_arr[0][1]
        back_default_text = flashcards_arr[0][2]

    flashcard_inputs = [
        [sg.Column([[sg.Button("Latex", key="add_latex")]], justification="right")],
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
            sg.Button("Save", key="save_flashcard"),
            sg.Button("View diagram", key="view_diagram"),
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

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event is not None:
            ### EVENTS FOR CLICK IN TABLES

            if (
                event[1] == "+CLICKED+"
                and (event[2][0] is not None and event[2][0] >= 0)
                and get_sources_list() != []
            ):
                row = event[2][0]

                set_front_input_selected(False)
                set_back_input_selected(False)

                match event[0]:
                    case "table_sources":
                        update_selected_source(window=window, row=row)
                    case "table_flashcards":
                        update_selected_flashcards(window=window, row=row)

            ###

            ### EVENTS FOR VIEWING AND LOADING diagram

            if event == "view_diagram":
                view_diagram(flashcard_id=get_selected_flashcard_id())

            ###

            ### EVENTS FOR FLASHCARD CHANGES

            if event in ["front_Enter", "back_Enter", "save_flashcard"]:
                update_flashcard(
                    flashcard_id=get_selected_flashcard_id(),
                    front=values["front"],
                    back=values["back"],
                )

                # To change only one flashcards I have to redraw all list.
                update_flashcards_table(window)

            check_input_click(event)

            if event == "add_latex":
                add_latex_to_input_field(window)

            if event == "preview_card":
                preview_card(text_front=values["front"], text_back=values["back"])

            ###

            ### MENU BAR EVENTS

            ## BOOK BAR EVENTS

            ### !!! CONTINUE WITH THE COMMENTS :D -C
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
                        "DELETE FROM sources WHERE id=?", (get_selected_source_id(),)
                    )
                    con.commit()
                    cursor.execute(
                        "DELETE FROM flashcards WHERE source_id=?",
                        (get_selected_source_id(),),
                    )
                    con.commit()

                    update_tables(window=window)

            if event == "Open source":
                filename = cursor.execute(
                    "SELECT filename FROM sources where id=?",
                    (get_selected_source_id(),),
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
                        "UPDATE sources SET filename=? WHERE id=?",
                        (
                            filename,
                            get_selected_source_id(),
                        ),
                    )
                    con.commit()
                else:
                    import webbrowser

                    webbrowser.open_new(filename)

            if event == "Change file":
                old_filename = cursor.execute(
                    "SELECT filename FROM sources where id=?",
                    (get_selected_source_id(),),
                ).fetchone()[0]
                filename = sg.popup_get_file(
                    "Please, select a file",
                    default_path=old_filename,
                    title="File selector",
                    file_types=(("Portable Document Format", "PDF"),),
                    keep_on_top=True,
                    modal=True,
                )

                if exists_filename(filename=filename):
                    cursor.execute(
                        "UPDATE sources SET filename=? WHERE id=?",
                        (
                            filename,
                            get_selected_source_id(),
                        ),
                    )
                    con.commit()

            ##

            ## CARD BAR EVENTS

            if event == "Add card":
                add_card()
                update_flashcards_table(window)
                update_selected_flashcards(window, len(get_flashcards_list()) - 1)
                window["table_flashcards"].Widget.see(len(get_flashcards_list()))
                if not cond_layout_flashcards_visible:
                    cond_layout_flashcards_visible = True

            if event == "Delete card":
                cursor.execute(
                    "DELETE FROM flashcards WHERE id=?", (get_selected_flashcard_id(),)
                )
                con.commit()
                update_flashcards_table(window)
                update_selected_flashcards(window, 0)
                window["table_flashcards"].Widget.see(1)

            if event == "Reschedule expired cards":
                today_str = datetime.now().strftime("%Y-%m-%d")
                cursor.execute(
                    "UPDATE flashcards SET deadline = ? WHERE deadline < ?",
                    (today_str, today_str),
                )
                con.commit()
                update_flashcards_table(window)
                update_selected_flashcards(window, 0)
                window["table_flashcards"].Widget.see(1)

            ##

            ###

    window.close()
