from setup import WEEKDAYS
from datetime import datetime as dt, timedelta as td
from termcolor import colored
import logging as log

# Create log for this script:
log.basicConfig(
    filename="logs/calc_deadline.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)

# Defining variables:
today_index = 0
pages_left = 0
days_to_add = 0


# ===================== #
# SUBTRACT PAGES METHOD #
# ===================== #
def subtract_pages(
    list_session_week: list,
    index_str: str,
):
    # Inheriting global variables:
    global today_index
    global pages_left
    global days_to_add

    if (
        list_session_week[WEEKDAYS[today_index]]["is_study_day"]
        and list_session_week[WEEKDAYS[today_index]]["are_there_sessions"]
    ):
        pages_left -= min(
            list_session_week[WEEKDAYS[today_index]][index_str], pages_left
        )

    # Going to next day:
    today_index += 1

    # If there are still pages to study, at least one more day is needed:
    if pages_left > 0:
        days_to_add += 1


# ========================= #
# CALCULATE DEADLINE METHOD #
# ========================= #
def calculate_deadline(
    list_session_week: list,
    total_pages: int | None = 0,
    studied_pages: int | None = 0,
) -> dt | str:
    """
    ## `calculate_deadline` method

    ===============================================

    #### `Description`

    This method calculates the deadline for the completion of a task like studying or exercising. \n
    The calculations are made taking into account how many study hours are available, how many pages
    (if needed) and similar parameters.

    ===============================================

    #### `Parameters`

    #####- `list_session_week`: `list`

    This list contains the weekly study plan. \n
    It is stored in db as `arr_session` and it depends on the user. \n
    It's created when a new source is inserted and its structure is: \n
    {
        `'total_pages'`: `int`, sum of each total_pages of all weekdays \n
        `'total_minutes'`: `int`, For the future \n
        `'total_duration'`: `int`, sum of each total_duration of all weekdays \n
        `'is_book'`: `True`/`False`, \n
        for `x` of WEEKDAYS: \n
            `x`:{ \n
                `'is_study_day'`: `True`/`False`, Check if x the user study (in general) \n
                `'are_there_sessions'`: True/False, Check if the user inserted sessions for this source \n
                `'amount'`: `int`, Numbers of sessions \n
                `'types'`: list, Its size is the amount, an element can be one of these ['Reading', 'Schematization', 'Testing'] \n
                `'durations'`: list, Its size is the amount, an element is an `int` between 0 and 59 (the length in minutes of the session) \n
                `'pages'`: list, Its size is the amount, an element is an `int` greater or equal 0 and corresponds to the pages of each sessions \n
                `'total_pages'`: `int`, sum(pages) \n
                `'total_duration'`: `int`, sum(durations) \n
                `'are_there_lectures'`: True/False, Check if x the user follows a lecture for this source \n
                `'time_lectures'`: { \n
                    `'time_start_date_lecture'`: "XX:XX", The start of the lecture \n
                    `'time_end_date_lecture'`: "XX:XX", The end of the lecture \n
                    `'duration_lecture'`: `int`, Timedelta in minutes, time_end_date_lecture - time_start_date_lecture \n
                } \n
            } \n
        `"with_lectures"`: True/False, Check if the user has associated lectures with the study of the source \n
       `"week_reps_lectures"`: `"BBBBBBB"`, B can be `0` or `1`. The i-th B says if the user inserted a lecture in i-th day of the week. \n
        `"start_date_lectures"`: `"XXXX-XX-XX"`, The start date of the lectures \n
        `"end_date_lectures"`: `"XXXX-XX-XX"`, The end date of the lecture \n
    } \n


    #####- `is_book`: `bool = True`

    This parameter checks if the source is a book or other type (video, audio).

    #####- `total_pages`: `int | None = 0`

    Number of pages needed to complete the source.

    #####- `studied_pages`: `int | None = 0`

    Number of pages already studied by the user.
    """

    global today_index
    global pages_left
    global days_to_add

    # Storing current date and day index:
    today_date = dt.now().date()
    today_index = today_date.weekday()

    deadline: dt = today_date

    # Calculating how many pages are left to study:
    pages_left = total_pages - studied_pages
    index_str = "total_pages"

    days_to_add = 0

    # Cycling through all the days of the week (Sunday has an index of 6):
    while today_index < 7:
        subtract_pages(list_session_week, index_str)

    # Adding the calculated days to the deadline:
    deadline += td(days=days_to_add)

    # Total pages (or minutes) of source during the week.
    # In the future index_str can be 'total_pages' or 'total_minutes'.
    # At the moment exists only the book version.
    week_todo = list_session_week[index_str]

    try:
        # Remaining week to complete the book; if it is greater than 0,
        # the value is reduced by 1 to have the exact day.
        weeks_add = int(pages_left / week_todo)

        if weeks_add > 0:
            weeks_add -= 1

        # Calculating how many days are needed to be added from the number of weeks.
        days_add = weeks_add * 7
        pages_left -= week_todo * weeks_add
        deadline += td(days=days_add)

        today_index = 0

        days_to_add = 0

        # Calculating how many days are needed to complete all the pages set in the goal:
        while pages_left > 0:
            subtract_pages(list_session_week, index_str)

            # If it's Sunday, go back to Monday:
            if today_index == 7:
                today_index = 0

        # Adding time to deadline:
        deadline += td(days=days_to_add)

        # Logging before returning:
        log.info(f"{dt.now}: Deadline calculated successfully. ")

        # Final output will be a datetime object:
        return deadline

    except ZeroDivisionError as e:
        # Logging before returning:
        log.info(f"{dt.now}: An ERROR occurred: {e}")
        return "Insert sessions!"


def TestDeadline():
    no_pages_input = {
        "total_pages": 0,
        "total_minutes": 0,
        "total_duration": 0,
        "is_book": True,
        "MON": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "TUE": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "WED": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "THU": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "FRI": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "SAT": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "SUN": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "with_lectures": False,
    }

    pages_100_no_plan_ideal_result = "Insert sessions!"
    pages_100_no_plan_true_result = calculate_deadline(
        list_session_week=no_pages_input, total_pages=100
    )
    if pages_100_no_plan_ideal_result != pages_100_no_plan_true_result:
        print(colored("Test. '100 pages no planned' failed!", "red"))
        print(
            colored(pages_100_no_plan_ideal_result, "red"),
            colored("!=", "red"),
            colored(pages_100_no_plan_true_result, "red"),
        )
    else:
        print(colored("Test. '100 pages no planned' success!", "green"))

    hundred_pages_monday_input = {
        "total_pages": 100,
        "total_minutes": 0,
        "total_duration": 55,
        "is_book": True,
        "MON": {
            "is_study_day": True,
            "are_there_sessions": True,
            "amount": 1,
            "types": ["Reading"],
            "durations": [
                55,
            ],
            "pages": [100, 0, 0, 0],
            "total_pages": 100,
            "total_duration": 55,
            "are_there_lectures": False,
        },
        "TUE": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "WED": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "THU": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "FRI": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "SAT": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "SUN": {
            "is_study_day": True,
            "are_there_sessions": False,
            "are_there_lectures": False,
        },
        "with_lectures": False,
    }

    pages_100_plan_all_in_monday_ideal_result = dt(
        day=6, month=11, year=2023
    ).date()  # Test for 2023-11-02
    pages_100_plan_all_in_monday_true_result = calculate_deadline(
        list_session_week=hundred_pages_monday_input, total_pages=100
    )
    if (
        pages_100_plan_all_in_monday_ideal_result
        != pages_100_plan_all_in_monday_true_result
    ):
        print(colored("Test. '100 pages planned in monday' failed!", "red"))
        print(
            colored(pages_100_plan_all_in_monday_ideal_result, "red"),
            colored("!=", "red"),
            colored(pages_100_plan_all_in_monday_true_result, "red"),
        )

    else:
        print(colored("Test. '100 pages planned in monday' success!", "green"))

    # TODO[Open][@ccritne] Find a strategy to get data of the user to create automatically new test
    import_input = {}
    import_input_ideal_result = ""
    import_input_true_result = ""
    if import_input_ideal_result != import_input_true_result:
        print(colored("Test. 'Import input' failed!", "red"))
        print(
            colored(import_input_ideal_result, "red"),
            colored("!=", "red"),
            colored(import_input_true_result, "red"),
        )

    else:
        print(colored("Test. 'Import input' success!", "green"))


TestDeadline()
