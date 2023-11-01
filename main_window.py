from functions import *
from browse_flashcards import browse_flashcards
from view_scheme import view_scheme
from today_flashcards import see_today_sessions
from to_do_list import see_to_do_list


def make_main_window():
    menu_layout = [
        [sg.Button("Deck & Flashcards", key="browse_flashcards", size=225)],
        [sg.Button("Check deadlines", key="deadlines", size=225)],
        [sg.Button("Today source session", key="todayStudySource", size=225)],
        [sg.Button("To-Do List", key="todolist", size=225)],
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
                key="deadlinesDeck",
            )
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("Menu", key="EVENT_MENU_Deadlines", size=225)],
    ]

    study_days = get_settings_value("study_days")

    settings_layout = [
        [
            sg.Text("Max study hour", size=(20, 1)),
            sg.Input(
                default_text=get_settings_value("maxStudyHour"),
                key="maxStudyHour",
                size=(5, 1),
            ),
        ],
        [
            sg.Text("Hour for Notification", size=(20, 1)),
            sg.Combo(
                [x for x in range(8, 24)],
                key="defaultHourNotification",
                default_value=get_settings_value("defaultHourNotification"),
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
        [
            sg.Checkbox(
                text="Mon",
                size=(6, 1),
                key="monSettings",
                default=bool(int(study_days[0])),
            ),
            sg.Checkbox(
                text="Fri",
                size=(6, 1),
                key="friSettings",
                default=bool(int(study_days[4])),
            ),
        ],
        [
            sg.Checkbox(
                text="Tue",
                size=(6, 1),
                key="tueSettings",
                default=bool(int(study_days[1])),
            ),
            sg.Checkbox(
                text="Sat",
                size=(6, 1),
                key="satSettings",
                default=bool(int(study_days[5])),
            ),
        ],
        [
            sg.Checkbox(
                text="Wed",
                size=(6, 1),
                key="wedSettings",
                default=bool(int(study_days[2])),
            ),
            sg.Checkbox(
                text="Sun",
                size=(6, 1),
                key="sunSettings",
                default=bool(int(study_days[6])),
            ),
        ],
        [
            sg.Checkbox(
                text="Thu",
                size=(6, 1),
                key="thuSettings",
                default=bool(int(study_days[3])),
            )
        ],
        [sg.HorizontalSeparator()],
        [sg.Button("Menu", key="EVENT_MENU_Settings")],
    ]

    menu_bar = [["File", "Exit"], ["Help", "About"]]

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

    window = sg.Window(title="StudyHelp", layout=layout, size=(300, 400), finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event is not None:
            ### START BINDING mENU_lAYOUT EVENTS
            if event == "flashcards":
                from_to("Menu", "Flashcards", window)

            if event == "deadlines":
                sources = cursor.execute(
                    "SELECT ID, name, deadline FROM sources"
                ).fetchall()
                window["deadlinesDeck"].update(values=sources)
                from_to("Menu", "Deadlines", window)

            if event == "settings":
                from_to("Menu", "Settings", window)

            if event == "todolist":
                see_to_do_list()

            if event == "todayStudySource":
                see_today_sessions()

            ### END BINDING mENU_lAYOUT EVENTS

            ### EVENTS BACK BUTTONS

            if "EVENT_BACK" in event:
                from_to(get_actual_page(), get_previous_page(), window)

            ###

            ### EVENTS FOR BROWSING FLASHCARDS AND DECKS

            if event == "browseFlashcards":
                browse_flashcards()

            ###

            ### MENU BUTTONS EVENT

            if "EVENT_MENU" in event:
                if "Settings" in event:
                    max_study_hour = int(values["maxStudyHour"])
                    default_hour_notification = int(values["defaultHourNotification"])
                    max_subjects_day = int(values["maxSubjectsDay"])

                    study_days = "".join(
                        [
                            str(int(window["monSettings"].get())),
                            str(int(window["tueSettings"].get())),
                            str(int(window["wedSettings"].get())),
                            str(int(window["thuSettings"].get())),
                            str(int(window["friSettings"].get())),
                            str(int(window["satSettings"].get())),
                            str(int(window["sunSettings"].get())),
                        ]
                    )

                    query = """UPDATE settings SET  maxStudyHour= ? , 
                                                    defaultHourNotification = ?, 
                                                    studyDays = ?,
                                                    maxSubjectsDay = ?"""

                    parameters = (
                        max_study_hour,
                        default_hour_notification,
                        study_days,
                        max_subjects_day,
                    )

                    cursor.execute(query, parameters)
                    con.commit()

                from_to(get_actual_page(), "Menu", window)
            ###

    window.close()
