# Imports
from datetime import date, datetime as dt, time, timedelta as td
import copy
import io
from io import BytesIO
import tkinter as tk
import matplotlib.pyplot as plt
from PIL import Image
import re
import ast
import textwrap
import base64
import os

# Global variables:
from tk_setup import *


# =========================== #
# CHANGE PREVIOUS PAGE METHOD #
# =========================== #
def change_previous_page(old_page: str):
    # Importing the variable from the setup file:
    global previous_page
    previous_page = old_page


# ======================== #
# GET PREVIOUS PAGE METHOD #
# ======================== #
def get_previous_page() -> str:
    global previous_page
    return previous_page


# ========================= #
# CHANGE ACTUAL PAGE METHOD #
# ========================= #
def change_actual_page(new_page: str):
    global actual_page
    actual_page = new_page


# ====================== #
# GET ACTUAL PAGE METHOD #
# ====================== #
def get_actual_page() -> str:
    global actual_page
    return actual_page


# ============== #
# FROM TO METHOD #
# ============== #
def from_to(str_from: str, str_to: str, frame: tk.Frame):
    pass  # I don't know what this class should do -M


# ========================= #
# CALCULATE DEADLINE METHOD #
# ========================= #
def calculate_deadline(
    list_session_week: list,
    is_book: bool = True,
    total_pages: int | None = 0,
    studied_pages: int | None = 0,
) -> dt:
    """
    ## `calculate_deadline` method

    ===============================================

    #### Description

    This method calculates the deadline for the completion of a task like studying or exercising.
    The calculations are made taking into account how many study hours are available, how many pages
    (if needed) and similar parameters.

    ===============================================

    #### Parameters

    #### - `list_session_week`: `list`

    This list contains the weekly study plan.

    #### - `is_book`: `bool = True`

    With a default value of True, this parameter checks if a book is used to achieve this task.

    #### - `total_pages`: `int | None = 0`

    Number of pages needed to complete the task.

    #### - `studied_pages`: `int | None = 0`

    Number of pages already studied by the user, that does not need to be taken into account.
    """
    # Storing current date and day index:
    today_date = dt.now()
    today_index = today_date.weekday()

    # Why the copy? - M
    deadline: dt = copy.copy(today_date)
    pages_left = 0

    index_str = ""

    if is_book:
        # Calculating how many pages are left to study:
        pages_left = total_pages - studied_pages
        index_str = "total_pages"

    days_to_add = 0

    # Cycling through all the days of the week (Sunday has an index of 6):
    while today_index < 7:
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

    # Adding the calculated days to the deadline:
    deadline += td(days=days_to_add)

    # Idk what this does, still have to understand what exactly will be list_session_week -M
    week_do = list_session_week[index_str]

    # same as above -M
    weeks_add = int(pages_left / week_do)

    if weeks_add > 0:
        weeks_add -= 1

    # Calculating how many days are needed to be added from the number of weeks.
    days_add = weeks_add * 7
    pages_left -= week_do * weeks_add
    deadline += td(days=days_add)

    today_index = 0

    days_to_add = 0

    # Calculating how many days are needed to complete all the pages set in the goal:
    while pages_left > 0:
        if (
            list_session_week[WEEKDAYS[today_index]]["is_study_day"]
            and list_session_week[WEEKDAYS[today_index]]["are_there_sessions"]
        ):
            pages_left -= min(
                list_session_week[WEEKDAYS[today_index]][index_str], pages_left
            )

        # If it's not Sunday, go forward in the week; if it's Sunday, go back to Monday:
        if today_index < 6:
            today_index += 1
        else:
            today_index = 0

        # If there are still pages left to study, add a day:
        if pages_left > 0:
            days_to_add += 1

    # Adding time to deadline:
    deadline += td(days=days_to_add)

    # Final output will be a datetime object:
    return deadline
