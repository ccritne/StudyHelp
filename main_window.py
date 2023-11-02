from functions import *
from browse_flashcards import browse_flashcards
from view_scheme import view_scheme
from today_flashcards import see_today_sessions
from to_do_list import see_to_do_list


def make_main_window():
    """
    It creates and display the principal menù with buttons:
    1. Browse
    2. Deadlines
    3. Today session
    4. To-Do
    5. Settings
    """
    menu_layout = [
        [sg.Button("Deck & Flashcards", key="browse_flashcards", size=225)],
        [sg.Button("Check deadlines", key="deadlines", size=225)],
        [sg.Button("Today source session", key="today_study_source", size=225)],
        [sg.Button("To-Do List", key="to_do_list", size=225)],
        [sg.Button("Settings", key="settings", size=225)],
    ]

    deadlines_layout = [
        [
            sg.Table(
                values=[],
                headings=["ID", "Source Name", "Deadline"],
                hide_vertical_scroll=True,
                justification="center",
                select_mode="none",
                key="deadlines_deck",
            )
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("Menu", key="EVENT_MENU_Deadlines", size=225)],
    ]

    # String's value at index i corresponds to decision of the WEEKDAY[I]
    # to study or rest (0=Rest, 1=Study)
    study_days = get_settings_value("study_days")

    settings_layout = [
        [
            sg.Text("Max study hour", size=(20, 1)),
            sg.Input(
                default_text=get_settings_value("max_study_hour"),
                key="max_study_hour",
                size=(5, 1),
            ),
        ],
        [
            sg.Text("Hour for Notification", size=(20, 1)),
            sg.Combo(
                [x for x in range(8, 24)],
                key="default_hour_notification",
                default_value=get_settings_value("default_hour_notification"),
                size=(3, 1),
            ),
        ],
        [
            sg.Text("Max subjects for day", size=(20, 1)),
            sg.Combo(
                [x for x in range(1, 4)],
                key="max_subjects_day",
                default_value=get_settings_value("max_subjects_day"),
                size=(3, 1),
            ),
        ],
        [sg.Text("Days ")],
        # The checkboxes's disposition is ugly but it allows to see all days in one window
        [
            sg.Checkbox(
                text=WEEKDAYS[0],
                size=(6, 1),
                key="mon_settings",
                default=bool(int(study_days[0])),
            ),
            sg.Checkbox(
                text=WEEKDAYS[4],
                size=(6, 1),
                key="fri_settings",
                default=bool(int(study_days[4])),
            ),
        ],
        [
            sg.Checkbox(
                text=WEEKDAYS[1],
                size=(6, 1),
                key="tue_settings",
                default=bool(int(study_days[1])),
            ),
            sg.Checkbox(
                text=WEEKDAYS[5],
                size=(6, 1),
                key="sat_settings",
                default=bool(int(study_days[5])),
            ),
        ],
        [
            sg.Checkbox(
                text=WEEKDAYS[2],
                size=(6, 1),
                key="wed_settings",
                default=bool(int(study_days[2])),
            ),
            sg.Checkbox(
                text=WEEKDAYS[6],
                size=(6, 1),
                key="sun_settings",
                default=bool(int(study_days[6])),
            ),
        ],
        [
            sg.Checkbox(
                text=WEEKDAYS[3],
                size=(6, 1),
                key="thu_settings",
                default=bool(int(study_days[3])),
            )
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("Menu", key="EVENT_MENU_Settings")],
    ]

    menu_bar = [["File", "Exit"], ["Help", "About"]]

    # Layout of all layouts.
    # PySimpleGUI doesn't allow to add dynamically layout or elements so I have to
    # hide the previous layout and show the next layout to simulate the
    # effect
    layout = [
        [sg.Menu(menu_bar)],
        [
            sg.Column(
                menu_layout,
                visible=True,
                key="Menu",
                justification="center",
                vertical_alignment="center",
            ),
            sg.Column(
                deadlines_layout, visible=False, key="Deadlines", justification="center"
            ),
            sg.Column(
                settings_layout, visible=False, key="Settings", justification="center"
            ),
        ],
    ]

    window = sg.Window(
        title="Study Help", layout=layout, size=(300, 400), finalize=True, modal=True
    )

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event is not None:
            ### START BINDING mENU_lAYOUT EVENTS
            if event == "flashcards":
                from_to("Menu", "Flashcards", window)

            if event == "deadlines":
                # Fill the tables of deadlines
                sources = cursor.execute(
                    "SELECT id, name, deadline FROM sources"
                ).fetchall()
                window["deadlines_deck"].update(values=sources)
                from_to("Menu", "Deadlines", window)

            if event == "settings":
                from_to("Menu", "Settings", window)

            if event == "to_do_list":
                see_to_do_list()

            if event == "today_study_source":
                see_today_sessions()

            ### END BINDING mENU_lAYOUT EVENTS

            ### EVENTS BACK BUTTONS

            if "EVENT_BACK" in event:
                from_to(get_actual_page(), get_previous_page(), window)

            ###

            ### EVENTS FOR BROWSING FLASHCARDS AND DECKS

            if event == "browse_flashcards":
                browse_flashcards()

            ###

            ### MENU BUTTONS EVENT

            if "EVENT_MENU" in event:
                if "Settings" in event:
                    # It saves the values of settings.
                    # It can avoid one query but they are only 4 values so is useless
                    # and it is better like this
                    max_study_hour = int(values["max_study_hour"])
                    default_hour_notification = int(values["default_hour_notification"])
                    max_subjects_day = int(values["max_subjects_day"])

                    study_days = "".join(
                        [
                            str(int(window["mon_settings"].get())),
                            str(int(window["tue_settings"].get())),
                            str(int(window["wed_settings"].get())),
                            str(int(window["thu_settings"].get())),
                            str(int(window["fri_settings"].get())),
                            str(int(window["sat_settings"].get())),
                            str(int(window["sun_settings"].get())),
                        ]
                    )

                    cursor.execute(
                        """UPDATE settings SET  max_study_hour= ? , 
                                                    default_hour_notification = ?, 
                                                    study_days = ?,
                                                    max_subjects_day = ?""",
                        (
                            max_study_hour,
                            default_hour_notification,
                            study_days,
                            max_subjects_day,
                        ),
                    )
                    con.commit()

                from_to(get_actual_page(), "Menu", window)
            ###

    window.close()
