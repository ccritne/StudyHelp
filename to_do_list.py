from functions import *


def preview_event(information: list):
    id = information[0]
    title = information[10]
    type = information[1]
    start_time = information[5]
    end_time = information[6]
    start_session = information[7]
    end_session = information[8]

    arr_start = ["", ""]
    if start_time not in ["", None]:
        arr_start = start_time.split(":")

    default_start_hour = arr_start[0]
    default_start_minute = arr_start[1]

    arr_end = ["", ""]
    if end_time not in ["", None]:
        arr_end = end_time.split(":")

    default_end_hour = arr_end[0]
    default_end_minute = arr_end[1]

    layout = [
        [
            [
                sg.Combo(
                    [from_number_to_time(x) for x in range(1, 24)],
                    key="START_HOUR",
                    size=(3, 1),
                    enable_events=True,
                    default_value=default_start_hour,
                ),
                sg.Text(":", size=(1, 1)),
                sg.Combo(
                    [from_number_to_time(x) for x in range(0, 60)],
                    key="START_MINUTE",
                    size=(3, 1),
                    enable_events=True,
                    default_value=default_start_minute,
                ),
                sg.Text("-", size=(1, 1)),
                sg.Combo(
                    [from_number_to_time(x) for x in range(10, 24)],
                    key="END_HOUR",
                    size=(3, 1),
                    enable_events=True,
                    default_value=default_end_hour,
                ),
                sg.Text(":", size=(1, 1)),
                sg.Combo(
                    [from_number_to_time(x) for x in range(0, 60)],
                    key="END_MINUTE",
                    size=(3, 1),
                    enable_events=True,
                    default_value=default_end_minute,
                ),
            ],
            [sg.Text("")][sg.HorizontalSeparator()],
            [sg.Button("Save", key="SAVE_EVENT")],
        ],
    ]

    window = sg.Window(
        title="Preview", layout=layout, finalize=True, modal=True, keep_on_top=True
    )

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event is not None:
            if (
                "START_HOUR" in event
                or "START_MINUTE" in event
                or "END_HOUR" in event
                or "END_MINUTE" in event
            ):
                event_key = copy.copy(event)

                eventFocus = "START_HOUR"
                if "START_MINUTE" in event:
                    eventFocus = "START_MINUTE"
                if "END_HOUR" in event:
                    eventFocus = "END_HOUR"
                if "END_MINUTE" in event:
                    eventFocus = "END_MINUTE"

                start_hour_key = event_key.replace(eventFocus, "START_HOUR")
                start_minute_key = event_key.replace(eventFocus, "START_MINUTE")
                end_hour_key = event_key.replace(eventFocus, "END_HOUR")
                end_minute_key = event_key.replace(eventFocus, "END_MINUTE")

                # Why defining a method inside a while true? -M
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

                    new_min_range_start, new_max_range_start = 0, 60
                    new_min_range_end, new_max_range_end = 0, 60
                    if new_end_hour == start_hour:
                        new_start_minute = 0
                        new_end_minute = 10
                        new_min_range_start, new_max_range_start = 0, 10
                        new_min_range_end, new_max_range_end = 10, 60

                    window[start_minute_key].update(
                        values=[
                            from_number_to_time(x)
                            for x in range(new_min_range_start, new_max_range_start)
                        ],
                        value=from_number_to_time(new_start_minute),
                    )
                    window[end_minute_key].update(
                        values=[
                            from_number_to_time(x)
                            for x in range(new_min_range_end, new_max_range_end)
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


def see_to_do_list():
    if get_selected_date() is None:
        dt = datetime.combine(datetime.now(), time(0, 0))
        set_selected_date(dt)

    def get_to_do_data_of(date: datetime):
        date_str = get_string_date(date)
        query = f"""SELECT calendar.id, 
                            sources.course_name,
                            sources.name, 
                            calendar.type,
                            calendar.description,
                            calendar.time_start_date,
                            calendar.time_end_date,
                            calendar.start_session,
                            calendar.end_session
                    FROM calendar 
                    LEFT JOIN 
                    sources ON source_id = sources.id 
                    WHERE date = ? 
                    ORDER BY inserted_day
                """
        parameters = (date_str,)

        cursor.execute(query, parameters)
        result = cursor.fetchall()

        rows = []
        for x in range(len(result)):
            row = [result[x][0], "", "", "", "", "", "", "", ""]
            for j in range(1, len(result[x])):
                if result[x][j] is not None:
                    row[j] = result[x][j]
            rows.append(row)

        return rows

    todo_list = get_to_do_data_of(get_selected_date())

    layout = [
        [
            sg.InputText(
                key="selected_date",
                default_text=get_string_date(get_selected_date()),
                size=(10, 1),
            ),
            sg.Button("Select day", key="select_to_do_date"),
        ],
        [
            sg.Table(
                values=todo_list,
                headings=[
                    "ID",
                    "Course",
                    "Source Title",
                    "Type",
                    "Description",
                    "Start",
                    "End",
                    "Start session",
                    "End session",
                ],
                key="to_do_list",
                auto_size_columns=False,
                expand_y=True,
                expand_x=True,
                col_widths=[5, 15, 15, 10, 10, 5, 5, 10, 10],
                justification="center",
                enable_click_events=True,
            )
        ],
    ]

    window = sg.Window(
        title="TODO List", layout=layout, finalize=True, modal=True, keep_on_top=True
    )

    window["selected_date"].bind("<Return>", "_Enter")

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event is not None:
            if event[1] == "+CLICKED+" and (
                event[2][0] is not None and event[2][0] >= 0
            ):
                information = todo_list[event[2][0]]
                preview_event(information)

            if event in ["select_to_do_date", "selected_date_Enter"]:
                sDate = values["selected_date"]

                if event == "select_to_do_date":
                    dtMon = datetime.now().month
                    selected_date = sg.popup_get_date(
                        close_when_chosen=True,
                        start_mon=dtMon,
                        no_titlebar=False,
                        modal=True,
                        keep_on_top=True,
                    )
                    sDate = (
                        from_number_to_time(selected_date[2])
                        + "-"
                        + from_number_to_time(selected_date[0])
                        + "-"
                        + from_number_to_time(selected_date[1])
                    )

                set_selected_date(datetime.strptime(sDate, "%Y-%m-%d"))

                window["selected_date"].update(
                    value=get_string_date(get_selected_date())
                )
                todo_list = get_to_do_data_of(get_selected_date())
                window["to_do_list"].update(values=todo_list)

    window.close()
