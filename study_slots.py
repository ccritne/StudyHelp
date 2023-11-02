from functions import *


def check_add_lecture_slot(
    index_day: int, hour: int, minute: int, duration_minutes: int, except_id: int = None
):
    query = "SELECT arr_sessions FROM sources "
    if except_id is not None:
        query += "WHERE id <> " + str(except_id)

    cursor.execute(query)
    result = cursor.fetchall()
    condition = True
    for x in result:
        json = ast.literal_eval(x)
        if json[WEEKDAYS[index_day]]["areThereLectures"]:
            arr_start_time = json[WEEKDAYS[index_day]]["timeLectures"][
                "time_start_date_lecture"
            ].split(":")
            arr_end_time = json[WEEKDAYS[index_day]]["timeLectures"][
                "time_end_date_lecture"
            ].split(":")
            minute_start = int(arr_start_time[0]) * 60 + int(arr_start_time[1])
            minute_end = int(arr_end_time[0]) * 60 + int(arr_end_time[1])

            # !!! FIX FIX FIX I have to understand when I can convalidate a slot :D
            condPUSH = True


def get_source_slots(defaults: dict = None):
    infos = {}

    rows = []

    default_start_date = ""
    default_end_date = ""

    if defaults != {} and defaults is not None:
        infos = copy.copy(defaults)
        if "start_date_lectures" in defaults and "end_date_lectures" in defaults:
            default_start_date = defaults["start_date_lectures"]
            default_end_date = defaults["end_date_lectures"]

    for x in range(7):
        weekday = WEEKDAYS[x]

        default_check = False

        default_start_hour = "09"
        default_start_minute = "00"
        default_end_hour = "10"
        default_end_minute = "30"

        if defaults != {} and defaults is not None and "with_lectures" in defaults:
            if (
                defaults["with_lectures"]
                and weekday in defaults
                and defaults[weekday]["are_there_lectures"]
            ):
                default_check = True

                arr_start = defaults[weekday]["time_lectures"][
                    "time_start_date_lecture"
                ].split(":")
                arr_end = defaults[weekday]["time_lectures"][
                    "time_end_date_lecture"
                ].split(":")

                default_start_hour = arr_start[0]
                default_start_minute = arr_start[1]
                default_end_hour = arr_end[0]
                default_end_minute = arr_end[1]

        row = [
            sg.Text(FULL_WEEKDAYS[x], size=(15, 1)),
            sg.Checkbox(
                "",
                key="CHECKBOX_" + (weekday),
                default=default_check,
                enable_events=True,
            ),
            sg.Column(
                [
                    [
                        sg.Combo(
                            [from_number_to_time(x) for x in range(1, 24)],
                            key="START_HOUR_" + (weekday),
                            size=(3, 1),
                            enable_events=True,
                            default_value=default_start_hour,
                        ),
                        sg.Text(":", size=(1, 1)),
                        sg.Combo(
                            [from_number_to_time(x) for x in range(0, 60)],
                            key="START_MINUTE_" + (weekday),
                            size=(3, 1),
                            enable_events=True,
                            default_value=default_start_minute,
                        ),
                        sg.Text("-", size=(1, 1)),
                        sg.Combo(
                            [from_number_to_time(x) for x in range(10, 24)],
                            key="END_HOUR_" + (weekday),
                            size=(3, 1),
                            enable_events=True,
                            default_value=default_end_hour,
                        ),
                        sg.Text(":", size=(1, 1)),
                        sg.Combo(
                            [from_number_to_time(x) for x in range(0, 60)],
                            key="END_MINUTE_" + (weekday),
                            size=(3, 1),
                            enable_events=True,
                            default_value=default_end_minute,
                        ),
                    ]
                ],
                visible=default_check,
                key="COLUMN_TIME_" + (weekday),
            ),
        ]
        rows.append(row)

    layout = [
        [
            sg.Input(
                disabled=True,
                key="start_lectures",
                size=(10, 1),
                default_text=default_start_date,
            ),
            sg.CalendarButton(
                "Start lectures", no_titlebar=False, format="%Y-%m-%d", size=(15, 1)
            ),
        ],
        [
            sg.Input(
                disabled=True,
                key="end_lectures",
                size=(10, 1),
                default_text=default_end_date,
            ),
            sg.CalendarButton(
                "End lectures", no_titlebar=False, format="%Y-%m-%d", size=(15, 1)
            ),
        ],
        [rows],
        [sg.Button("Save", key="SAVE_SLOTS")],
    ]

    window = sg.Window(
        "Set lecture slots", layout=layout, modal=True, finalize=True, keep_on_top=True
    )

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event is not None:
            if event == "SAVE_SLOTS":
                sum_of_lectures = 0

                for x in range(7):
                    if values["CHECKBOX_" + WEEKDAYS[x]]:
                        sum_of_lectures += 1

                if sum_of_lectures > 0:
                    infos["with_lectures"] = True
                    infos["week_reps_lectures"] = ""

                    infos["start_date_lectures"] = values["start_lectures"]
                    infos["end_date_lectures"] = values["end_lectures"]
                    for x in range(7):
                        infos[WEEKDAYS[x]] = {}
                        if values["CHECKBOX_" + WEEKDAYS[x]]:
                            infos[WEEKDAYS[x]]["are_there_lectures"] = True
                            infos["week_reps_lectures"] += "1"
                            infos[WEEKDAYS[x]]["time_lectures"] = {
                                "time_start_date_lecture": values[
                                    "START_HOUR_" + WEEKDAYS[x]
                                ]
                                + ":"
                                + values["START_MINUTE_" + WEEKDAYS[x]],
                                "time_end_date_lecture": values[
                                    "END_HOUR_" + WEEKDAYS[x]
                                ]
                                + ":"
                                + values["END_MINUTE_" + WEEKDAYS[x]],
                                "duration_lecture": (
                                    int(values["END_HOUR_" + WEEKDAYS[x]]) * 60
                                    + int(values["END_MINUTE_" + WEEKDAYS[x]])
                                )
                                - (
                                    int(values["START_HOUR_" + WEEKDAYS[x]]) * 60
                                    + int(values["START_MINUTE_" + WEEKDAYS[x]])
                                ),
                            }
                        else:
                            infos["week_reps_lectures"] += "0"
                            infos[WEEKDAYS[x]]["are_there_lectures"] = False
                else:
                    infos["with_lectures"] = False

                break

            if "CHECKBOX_" in event:
                event_key = copy.copy(event)
                weekday = event_key.replace("CHECKBOX_", "")

                window["COLUMN_TIME_" + weekday].update(visible=values[event_key])

            if (
                "START_HOUR_" in event
                or "START_MINUTE_" in event
                or "END_HOUR_" in event
                or "END_MINUTE_" in event
            ):
                event_key = copy.copy(event)

                event_focus = "START_HOUR_"
                if "START_MINUTE_" in event:
                    event_focus = "START_MINUTE_"
                if "END_HOUR_" in event:
                    event_focus = "END_HOUR_"
                if "END_MINUTE_" in event:
                    event_focus = "END_MINUTE_"

                start_hour_key = event_key.replace(event_focus, "START_HOUR_")
                start_minute_key = event_key.replace(event_focus, "START_MINUTE_")
                end_hour_key = event_key.replace(event_focus, "END_HOUR_")
                end_minute_key = event_key.replace(event_focus, "END_MINUTE_")

                def get_values(values, key):
                    new_val = 0
                    if values[key] not in [None, ""]:
                        new_val = int(values[key])
                    return new_val

                start_hour = get_values(values, start_hour_key)
                start_minute = get_values(values, start_minute_key)
                end_hour = get_values(values, end_hour_key)
                end_minute = get_values(values, end_minute_key)

                if start_hour > end_hour:
                    new_end_hour = min(start_hour + 1, 23)
                    window[end_hour_key].update(
                        values=[from_number_to_time(x) for x in range(start_hour, 24)],
                        value=from_number_to_time(min(start_hour + 1, 23)),
                    )

                    new_start_minute = 0
                    new_end_minute = 0

                    newMinRangeStart, newMaxRangeStart = 0, 60
                    newMinRangeEnd, newMaxRangeEnd = 0, 60
                    if new_end_hour == start_hour:
                        new_start_minute = 0
                        new_end_minute = 10
                        newMinRangeStart, newMaxRangeStart = 0, 10
                        newMinRangeEnd, newMaxRangeEnd = 10, 60

                    window[start_minute_key].update(
                        values=[
                            from_number_to_time(x)
                            for x in range(newMinRangeStart, newMaxRangeStart)
                        ],
                        value=from_number_to_time(new_start_minute),
                    )
                    window[end_minute_key].update(
                        values=[
                            from_number_to_time(x)
                            for x in range(newMinRangeEnd, newMaxRangeEnd)
                        ],
                        value=from_number_to_time(new_end_minute),
                    )
                else:
                    if start_hour == end_hour:
                        window[start_minute_key].update(
                            values=[
                                from_number_to_time(x) for x in range(0, end_minute)
                            ]
                        )

                        new_start_minute = max(end_minute - 1, 0)
                        if 0 <= start_minute < end_minute:
                            new_start_minute = start_minute

                        window[start_minute_key].update(
                            value=from_number_to_time(new_start_minute)
                        )
                        window[end_minute_key].update(
                            values=[
                                from_number_to_time(x)
                                for x in range(new_start_minute + 1, 60)
                            ]
                        )

                        new_end_minute = new_start_minute + 1
                        if new_start_minute + 1 <= end_minute < 60:
                            new_end_minute = end_minute

                        window[end_minute_key].update(
                            value=from_number_to_time(new_end_minute)
                        )

                    else:
                        window[end_hour_key].update(
                            values=[
                                from_number_to_time(x) for x in range(start_hour, 24)
                            ],
                            value=from_number_to_time(end_hour),
                        )
                        window[start_minute_key].update(
                            values=[from_number_to_time(x) for x in range(0, 60)],
                            value=from_number_to_time(start_minute),
                        )
                        window[end_minute_key].update(
                            values=[from_number_to_time(x) for x in range(0, 60)],
                            value=from_number_to_time(end_minute),
                        )

    window.close()

    return infos


def get_study_slots(
    study_days: str,
    arr_amount: str,
    is_book: bool = True,
    is_video: bool = False,
    defaults: list | None = None,
    source_id: int | None = None,
) -> list | None:
    combo_selection = ["Schematization", "Testing"]

    if is_video:
        combo_selection.insert(0, "Viewing")

    if is_book:
        combo_selection.insert(0, "Reading")

    rows = []

    for x in range(7):
        if study_days[x]:
            row = []

            for j in range(arr_amount[x]):
                default_pages = 0
                default_type = ""
                cond_type = False

                if is_video:
                    default_type = "Viewing"
                    cond_type = False

                if is_book:
                    default_pages = "10"
                    default_type = "Reading"
                    cond_type = True

                default_duration = 55

                if defaults and defaults is not None:
                    infos = copy.copy(defaults)

                    if (
                        "are_there_sessions" in defaults[WEEKDAYS[x]]
                        and defaults[WEEKDAYS[x]]["are_there_Sessions"]
                        and j < defaults[WEEKDAYS[x]]["amount"]
                    ):
                        default_type = defaults[WEEKDAYS[x]]["types"][j]

                        if is_book:
                            default_pages = defaults[WEEKDAYS[x]]["pages"][j]
                            default_duration = defaults[WEEKDAYS[x]]["durations"][j]
                            cond_type = True

                        if is_video:
                            default_duration = defaults[WEEKDAYS[x]]["minutes"][j]
                            cond_type = False

                        if default_type in ["Schematization"]:
                            cond_type = False

                lyt = [
                    sg.Frame(
                        str(f"{j+1}° Session"),
                        [
                            [
                                sg.Text(
                                    "Pages: ",
                                    size=(12, 1),
                                    visible=cond_type,
                                    key=f"TEXT_PAGES_{j}_SESSION_{WEEKDAYS[x]}",
                                ),
                                sg.InputText(
                                    default_text=default_pages,
                                    key=f"INPUT_TEXT_PAGES_{j}_SESSION_{WEEKDAYS[x]}",
                                    size=(5, 1),
                                    visible=cond_type,
                                ),
                            ],
                            [
                                sg.Text("Type: ", size=(12, 1)),
                                sg.Combo(
                                    combo_selection,
                                    size=(13, 1),
                                    default_value=default_type,
                                    key=f"COMBO_TYPE_{j}_SESSION_{WEEKDAYS[x]}",
                                    enable_events=True,
                                ),
                            ],
                            [
                                sg.Text("Duration: ", size=(12, 1)),
                                sg.Combo(
                                    [x for x in range(1, 61, 1)],
                                    default_value=default_duration,
                                    tooltip="Minutes",
                                    key=f"INPUT_TEXT_DURATION_{j}_SESSION_{WEEKDAYS[x]}",
                                    size=(3, 1),
                                    readonly=True,
                                ),
                            ],
                        ],
                    )
                ]

                row.append(lyt)

            frame = [sg.Frame(FULL_WEEKDAYS[x], row)]
            rows.append(frame)

    column = sg.Column(
        rows, scrollable=True, vertical_scroll_only=True, size=(None, 350)
    )

    layout = [[column], [sg.Button("Save", key="SAVE_SLOTS")]]

    window = sg.Window(
        "Set study slots", layout=layout, modal=True, finalize=True, keep_on_top=True
    )

    infos = {}

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event is not None:
            if "COMBO_TYPE_" in event:
                combo_key = copy.copy(event)
                cond_type = False
                if is_book and values[combo_key] in ["Reading", "Testing"]:
                    cond_type = True

                input_pages_key = combo_key.replace("COMBO_TYPE_", "INPUT_TEXT_PAGES_")
                display_pages_key = combo_key.replace("COMBO_TYPE_", "TEXT_PAGES_")

                window[display_pages_key].update(visible=cond_type)
                window[input_pages_key].update(visible=cond_type)

            if event == "SAVE_SLOTS":
                infos["total_pages"] = 0
                infos["total_minutes"] = 0
                infos["total_duration"] = 0
                infos["is_book"] = is_book

                max_study_hour = get_settings_value("max_study_hour")

                cond_error_hours = False
                cond_error_hours_index = False
                error_text_hours = f"Max study hours allowed are {max_study_hour}.\n"

                for x in range(7):
                    cond_error_hours_index = False
                    infos[WEEKDAYS[x]] = {}
                    if study_days[x]:
                        infos[WEEKDAYS[x]]["is_study_day"] = True
                        infos[WEEKDAYS[x]]["are_there_sessions"] = False
                        if arr_amount[x] > 0:
                            infos[WEEKDAYS[x]]["are_there_sessions"] = True
                            infos[WEEKDAYS[x]]["amount"] = arr_amount[x]
                            infos[WEEKDAYS[x]]["types"] = []
                            infos[WEEKDAYS[x]]["durations"] = []

                            if is_book:
                                infos[WEEKDAYS[x]]["pages"] = []
                                infos[WEEKDAYS[x]]["totalPages"] = 0

                            infos[WEEKDAYS[x]]["total_duration"] = 0
                            for j in range(arr_amount[x]):
                                if is_book:
                                    pages = int(
                                        values[
                                            f"INPUT_TEXT_PAGES_{j}_SESSION_{WEEKDAYS[x]}"
                                        ]
                                    )
                                    type_study = values[
                                        f"COMBO_TYPE_{j}_SESSION_{WEEKDAYS[x]}"
                                    ]

                                    if type_study in ["Schematization"]:
                                        pages = 0

                                    infos[WEEKDAYS[x]]["pages"].append(pages)
                                    infos[WEEKDAYS[x]]["total_pages"] += pages
                                    infos["total_pages"] += pages
                                else:
                                    minutes = int(
                                        values[
                                            f"INPUT_TEXT_DURATION_{j}_SESSION_{WEEKDAYS[x]}"
                                        ]
                                    )
                                    type_study = values[
                                        f"COMBO_TYPE_{j}_SESSION_{WEEKDAYS[x]}"
                                    ]

                                    if type_study in ["Schematization"]:
                                        minutes = 0

                                    infos[WEEKDAYS[x]]["minutes"].append(minutes)
                                    infos[WEEKDAYS[x]]["total_minutes"] += minutes
                                    infos["total_minutes"] += minutes

                                duration = int(
                                    values[
                                        f"INPUT_TEXT_DURATION_{j}_SESSION_{WEEKDAYS[x]}"
                                    ]
                                )
                                infos[WEEKDAYS[x]]["types"].append(
                                    values[f"COMBO_TYPE_{j}_SESSION_{WEEKDAYS[x]}"]
                                )
                                infos[WEEKDAYS[x]]["durations"].append(duration)
                                infos[WEEKDAYS[x]]["total_duration"] += duration
                                infos["total_duration"] += duration

                                old_total_minutes = get_total_minutes(x)
                                if source_id is not None:
                                    old_total_minutes = get_total_minutes(
                                        x, except_id=source_id
                                    )

                                new_total_minutes = (
                                    old_total_minutes
                                    + infos[WEEKDAYS[x]]["total_duration"]
                                )
                                total_hours = new_total_minutes / 60

                                if (
                                    total_hours > max_study_hour
                                    and not cond_error_hours_index
                                ):
                                    cond_error_hours = True
                                    cond_error_hours_index = True
                                    error_text_hours += (
                                        "You have to correct "
                                        + FULL_WEEKDAYS[x]
                                        + " sessions. Your hour amounts is "
                                        + f"{total_hours:.2f}.\n"
                                    )
                    else:
                        infos[WEEKDAYS[x]]["is_study_day"] = False

                if True in [cond_error_hours]:
                    if cond_error_hours:
                        sg.popup_error(
                            error_text_hours,
                            title="Too much hours",
                            modal=True,
                            keep_on_top=True,
                        )
                else:
                    break

    window.close()
    return infos
