from functions import *
from study_slots import *
from setup import WEEKDAYS


def update_deadline(
    window: sg.Window,
    values: dict,
    study_slots_info: dict,
    is_book: bool = True,
):
    if is_book:
        number_pages_str = values["number_pages"]
        studied_pages_str = values["entryStudied_pages"]
        if check_str_int_input(number_pages_str) and check_str_int_input(
            studied_pages_str
        ):
            number_pages = int(number_pages_str)
            studied_pages = int(studied_pages_str)
            if number_pages > 0 and studied_pages >= 0:
                if study_slots_info is not None:
                    window["previewDeadline"].update(
                        value=get_string_date(
                            calculate_deadline(
                                is_book=is_book,
                                arr_session_week=study_slots_info,
                                total_pages=number_pages,
                                studied_pages=studied_pages,
                            )
                        )
                    )
            else:
                window["previewDeadline"].update(value="Check values!")


def creation_events(
    command: str,
    study_slots_info: list,
    last_page: int,
    with_lectures: bool,
    deadline: datetime,
):
    ### Creation of events
    last_ID = None

    if command == "NEW":
        last_ID = cursor.execute("SELECT MAX(ID) FROM SOURCES").fetchone()[0]

    if command == "MODIFY":
        # Deletion of future events
        last_ID = get_selected_source_ID()
        iter_day = datetime.now()
        sql = "DELETE FROM calendar WHERE date >= ? AND source_ID = ?"
        parameters = (get_string_date(iter_day), last_ID)
        cursor.execute(sql, parameters)
        con.commit()

    iter_day = datetime.now()
    insert_date = get_string_date(datetime.now())
    days = (deadline - iter_day).days + 1
    iter = 0
    index_week = datetime.now().weekday()
    sql = "INSERT INTO CALENDAR(type, insertedDay, date, startSession, endSession, source_ID) VALUES \n"

    while iter <= days:
        if (
            study_slots_info[WEEKDAYS[index_week]]["isStudyDay"]
            and study_slots_info[WEEKDAYS[index_week]]["areThereSessions"]
        ):
            iter_day_str = get_string_date(iter_day)
            for x in range(study_slots_info[WEEKDAYS[index_week]]["amount"]):
                study_type = study_slots_info[WEEKDAYS[index_week]]["types"][x]

                sql += (
                    "('"
                    + study_type
                    + "', '"
                    + insert_date
                    + "', '"
                    + iter_day_str
                    + "'"
                )

                start_page = last_page
                end_page = (
                    start_page + study_slots_info[WEEKDAYS[index_week]]["pages"][x]
                )
                last_page = end_page

                if study_type in ["Schematization"]:
                    start_page = "NULL"
                    end_page = "NULL"

                sql += (
                    ", "
                    + str(start_page)
                    + ", "
                    + str(end_page)
                    + ", "
                    + str(last_ID)
                    + "),"
                )

        index_week += 1

        if index_week == 7:
            index_week = 0

        iter += 1

        iter_day += timedelta(days=1)

    sql = sql[: len(sql) - 1] + ";"

    cursor.execute(sql)
    con.commit()

    if with_lectures:
        sql = "INSERT INTO calendar(type, insertedDay, date, timeStartDate, timeEndDate, source_ID) VALUES \n"
        iter_day = datetime.strptime(study_slots_info["startDateLectures"], "%Y-%m-%d")
        insert_date = get_string_date(datetime.now())
        deadline_lectures = study_slots_info["endDateLectures"]
        days = (datetime.strptime(deadline_lectures, "%Y-%m-%d") - iter_day).days
        iter = 0
        index_week = iter_day.weekday()

        while iter <= days:
            if study_slots_info[WEEKDAYS[index_week]]["areThereLectures"]:
                sql += (
                    "('Lecture', '"
                    + insert_date
                    + "','"
                    + get_string_date(iter_day)
                    + "', '"
                    + study_slots_info[WEEKDAYS[index_week]]["timeLectures"][
                        "timeStartDateLecture"
                    ]
                    + "', '"
                    + study_slots_info[WEEKDAYS[index_week]]["timeLectures"][
                        "timeEndDateLecture"
                    ]
                    + "', "
                    + str(last_ID)
                    + "),"
                )

            index_week += 1

            if index_week == 7:
                index_week = 0

            iter += 1

            iter_day += timedelta(days=1)

        sql = sql[: len(sql) - 1] + ";"
        cursor.execute(sql)
        con.commit()


def update_source(command: str = "NEW"):
    study_days = [bool(int(x)) for x in get_settings_value("study_days")]

    study_slots_info = {}

    default_name = ""

    default_today_date_str = datetime.now().strftime("%Y-%m-%d")

    sessions = ["0", "0", "0", "0", "0", "0", "0"]

    button_text = "ADD"
    window_title = "ADD NEW SOURCE"

    with_lectures = False
    default_name_course = ""

    is_book = True
    is_video = False

    default_total_pages = 100
    default_studied_pages = 0

    default_path_file = ""

    default_deadline = "Insert sessions!"

    if command == "MODIFY":
        source_values = get_source_values(get_selected_source_ID())

        study_slots_info = ast.literal_eval(source_values[7])

        def update_default_value(old_value, source_values, index):
            if source_values[index] is not None:
                return source_values[index]

            return old_value

        default_name_course = update_default_value(
            default_name_course, source_values, 1
        )

        default_name = update_default_value(default_name, source_values, 2)
        default_total_pages = update_default_value(default_name, source_values, 3)
        default_studied_pages = update_default_value(
            default_studied_pages, source_values, 4
        )
        default_path_file = update_default_value(default_path_file, source_values, 5)
        default_deadline = update_default_value(default_deadline, source_values, 6)

        for x in range(7):
            if (
                study_slots_info[WEEKDAYS[x]]["isStudyDay"]
                and study_slots_info[WEEKDAYS[x]]["areThereSessions"]
            ):
                sessions[x] = str(study_slots_info[WEEKDAYS[x]]["amount"])
            else:
                sessions[x] = "0"

        with_lectures = study_slots_info["with_lectures"]

        button_text = "MODIFY"
        window_title = "MODIFY BOOK"

    column_group = [
        [
            sg.Text("Day", size=(5, 1), justification="center"),
            sg.Text("Sessions", size=(10, 1), justification="center"),
            sg.Text("Minutes left", size=(10, 1), justification="center"),
        ]
    ]

    for x in range(7):
        if study_days[x]:
            max_study_hour = get_settings_value("maxStudyHour")
            total_minutes = get_total_minutes(x)
            remaining_minutes = max_study_hour * 60 - total_minutes

            row = [
                sg.Text(text=WEEKDAYS[x], size=(5, 1)),
                sg.InputText(
                    size=(10, 1),
                    justification="center",
                    default_text=sessions[x],
                    enable_events=True,
                    key="INPUT_TEXT_SESSIONS_" + WEEKDAYS[x],
                ),
                sg.Text(
                    text=remaining_minutes,
                    size=(10, 1),
                    justification="center",
                    key="DISPLAY_TIME_REMAINING_" + WEEKDAYS[x],
                ),
            ]
            column_group.append(row)

    layout = [
        [
            sg.Text("Name "),
            sg.Input(key="nameDeck", default_text=default_name, expand_x=True),
        ],
        [
            sg.Checkbox(
                "Associate with lectures?",
                default=with_lectures,
                key="checkboxLectures",
                enable_events=True,
            ),
            sg.Text(
                "Name course: ", key="DISPLAY_TEXT_NAME_COURSE", visible=with_lectures
            ),
            sg.Input(
                key="INPUT_TEXT_NAME_COURSE",
                default_text=default_name_course,
                visible=with_lectures,
            ),
            sg.Button("Insert slots", disabled=not with_lectures, key="btnSlots"),
        ],
        [sg.HorizontalSeparator()],
        [sg.Column(column_group, justification="center")],
        [sg.Button("Study slots", key="STUDY_SLOTS", expand_x=True)],
        [sg.HorizontalSeparator()],
        [
            sg.Text(
                "Number of pages ",
                size=(20, 1),
                visible=is_book,
                key="textNumber_pages",
            ),
            sg.Input(
                key="number_pages",
                default_text=default_total_pages,
                justification="center",
                size=(4, 1),
                enable_events=True,
                visible=is_book,
            ),
        ],
        [
            sg.Text(
                "Number of studied pages ",
                size=(20, 1),
                visible=is_book,
                key="textStudied_pages",
            ),
            sg.Input(
                key="entryStudied_pages",
                default_text=default_studied_pages,
                justification="center",
                size=(4, 1),
                enable_events=True,
                visible=is_book,
            ),
        ],
        [
            sg.Text("Document ", size=(20, 1)),
            sg.Input(key="pathSource", size=(10, 1), default_text=default_path_file),
            sg.FileBrowse(
                file_types=(("Portable Document Format", "PDF"),), visible=is_book
            ),
        ],
        [
            sg.Text("Deadline ", size=(20, 1)),
            sg.Input(
                key="previewDeadline",
                size=(10, 1),
                default_text=default_deadline,
                readonly=True,
            ),
        ],
        [sg.Button(button_text, key="update_source", expand_x=True)],
    ]

    window = sg.Window(
        window_title, layout=layout, modal=True, finalize=True, keep_on_top=True
    )

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event is not None:
            if event in ["number_pages", "entryStudied_pages"]:
                update_deadline(
                    is_book=is_book,
                    window=window,
                    values=values,
                    study_slots_info=study_slots_info,
                )

            if event == "STUDY_SLOTS":
                arr_amounts = []
                book_study_days = []

                sum_of_amount = 0

                for x in range(7):
                    if study_days[x]:
                        amount = int(values[f"INPUT_TEXT_SESSIONS_{WEEKDAYS[x]}"])
                        arr_amounts.append(amount)
                        book_study_days.append(True)
                        sum_of_amount += amount
                    else:
                        arr_amounts.append(0)
                        book_study_days.append(False)

                if sum_of_amount > 0:
                    if command == "NEW":
                        study_slots_info = get_study_slots(
                            is_book=is_book,
                            is_video=is_video,
                            study_days=book_study_days,
                            arr_amount=arr_amounts,
                            defaults=study_slots_info,
                        )
                    if command == "MODIFY":
                        study_slots_info = get_study_slots(
                            is_book=is_book,
                            is_video=is_video,
                            study_days=book_study_days,
                            arr_amount=arr_amounts,
                            defaults=study_slots_info,
                            source_ID=get_selected_source_ID(),
                        )

                    update_deadline(
                        is_book=is_book,
                        window=window,
                        values=values,
                        study_slots_info=study_slots_info,
                    )

                    for x in range(7):
                        if (
                            study_slots_info[WEEKDAYS[x]]["isStudyDay"]
                            and study_slots_info[WEEKDAYS[x]]["areThereSessions"]
                        ):
                            max_study_hour = get_settings_value("maxStudyHour")
                            total_minutes = (
                                get_total_minutes(x, exceptID=get_selected_source_ID())
                                + study_slots_info[WEEKDAYS[x]]["totalDuration"]
                            )
                            remaining_minutes = max_study_hour * 60 - total_minutes

                            window["DISPLAY_TIME_REMAINING_" + WEEKDAYS[x]].update(
                                value=remaining_minutes
                            )

                else:
                    sg.popup_ok(
                        "Insert almost one session!",
                        title="WARNING",
                        keep_on_top=True,
                        modal=True,
                    )

            if event == "update_source":
                name_book = values["nameDeck"]
                course_name = values["INPUT_TEXT_NAME_COURSE"]

                if is_book:
                    query = "INSERT INTO sources(name, course_name, number_pages, studied_pages, filename, arrSessions, deadline, insert_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                    if command == "MODIFY":
                        query = "UPDATE sources SET name = ?, course_name = ?, number_pages = ?, studied_pages = ?, filename = ?, arrSessions = ?, deadline = ? WHERE ID = ?"

                    number_pages_str = values["number_pages"]
                    studied_pages_str = values["entryStudied_pages"]

                    filename = values["pathSource"]

                    if check_str_int_input(number_pages_str) and check_str_int_input(
                        studied_pages_str
                    ):
                        number_pages = int(number_pages_str)
                        studied_pages = int(studied_pages_str)

                        if number_pages > 0 and studied_pages >= 0:
                            if study_slots_info != {}:
                                deadline = calculate_deadline(
                                    is_book=is_book,
                                    arr_session_week=study_slots_info,
                                    total_pages=number_pages,
                                    studied_pages=studied_pages,
                                )

                                parameters = (
                                    name_book,
                                    course_name,
                                    number_pages,
                                    studied_pages,
                                    filename,
                                    str(study_slots_info),
                                    get_string_date(deadline),
                                )

                                if command == "MODIFY":
                                    parameters = parameters + (
                                        get_selected_source_ID(),
                                    )

                                if command == "NEW":
                                    parameters = parameters + (default_today_date_str,)

                                cursor.execute(query, parameters)
                                con.commit()

                                last_page = studied_pages + 1

                                creation_events(
                                    command=command,
                                    study_slots_info=study_slots_info,
                                    last_page=last_page,
                                    with_lectures=with_lectures,
                                    deadline=deadline,
                                )

                                break
                            else:
                                sg.popup_ok(
                                    "You have to set your study slots!",
                                    title="WARNING",
                                    keep_on_top=True,
                                    modal=True,
                                )
                        else:
                            sg.popup_ok(
                                "Please, set the correct values!",
                                title="WARNING",
                                keep_on_top=True,
                                modal=True,
                            )
                    else:
                        sg.popup_ok(
                            "Please, set the correct values!",
                            title="WARNING",
                            keep_on_top=True,
                            modal=True,
                        )

            if event == "checkboxLectures":
                with_lectures = values["checkboxLectures"]
                window["btnSlots"].update(disabled=not with_lectures)
                window["DISPLAY_TEXT_NAME_COURSE"].update(visible=with_lectures)
                window["INPUT_TEXT_NAME_COURSE"].update(visible=with_lectures)

            if event == "btnSlots":
                source_slots_info = get_source_slots(study_slots_info)

                study_slots_info["with_lectures"] = source_slots_info["with_lectures"]
                if study_slots_info["with_lectures"]:
                    study_slots_info["weekRepsLectures"] = source_slots_info[
                        "weekRepsLectures"
                    ]
                    study_slots_info["startDateLectures"] = source_slots_info[
                        "startDateLectures"
                    ]
                    study_slots_info["endDateLectures"] = source_slots_info[
                        "endDateLectures"
                    ]
                    for x in range(7):
                        if WEEKDAYS[x] not in study_slots_info:
                            study_slots_info[WEEKDAYS[x]] = {}

                        study_slots_info[WEEKDAYS[x]][
                            "areThereLectures"
                        ] = source_slots_info[WEEKDAYS[x]]["areThereLectures"]

                        if (
                            WEEKDAYS[x] in source_slots_info
                            and source_slots_info[WEEKDAYS[x]]["areThereLectures"]
                        ):
                            study_slots_info[WEEKDAYS[x]]["timeLectures"] = {
                                "timeStartDateLecture": source_slots_info[WEEKDAYS[x]][
                                    "timeLectures"
                                ]["timeStartDateLecture"],
                                "timeEndDateLecture": source_slots_info[WEEKDAYS[x]][
                                    "timeLectures"
                                ]["timeEndDateLecture"],
                                "durationLecture": source_slots_info[WEEKDAYS[x]][
                                    "timeLectures"
                                ]["durationLecture"],
                            }

    window.close()
