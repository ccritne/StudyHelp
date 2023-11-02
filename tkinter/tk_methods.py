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


# ============== #
# FROM TO METHOD #
# ============== #
def from_to(str_from: str, str_to: str, frame: tk.Frame):
    pass  # I don't know what this class should do -M


# ======================== #
# ALL SOURCES NAMES METHOD #
# ======================== #
def all_sources_names() -> list:
    """
    It returns IDs and names of sources.
    """
    cursor.execute("SELECT id, name FROM sources")
    result = cursor.fetchall()

    return result


# ===================== #
# GET INFO DECKS METHOD #
# ===================== #
def get_info_decks() -> list:
    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        f"""SELECT sources.id,
                                sources.name,
                                flashcards.deadline
                            FROM flashcards
                                LEFT JOIN
                                sources ON flashcards.source_id = sources.id
                            ORDER BY sources.id;
                        """
    )

    list = cursor.fetchall()
    if list != []:
        id = list[0][0]
        table_info = [[id, list[0][1], 0]]
        index = 0
        for x in range(len(list)):
            if list[x][0] != id:  # Sort fetch
                id = list[x][0]
                table_info.append([id, list[x][1], 0])
                index += 1

            if list[x][2] == today_str:
                table_info[index][2] += 1

        return table_info

    return [[]]


# ========================= #
# GET SETTINGS VALUE METHOD #
# ========================= #
def get_settings_value(value: str) -> str | int:
    cursor.execute("SELECT " + value + " FROM settings")

    return cursor.fetchone()[0]


# ! ================================================================================= ! #
# ! ================================================================================= ! #
# ! ================================== PAGE METHODS ================================= ! #
# ! ================================================================================= ! #
# ! ================================================================================= ! #


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


# ! ================================================================================= ! #
# ! ================================================================================= ! #
# ! ================================ DEADLINE METHODS =============================== ! #
# ! ================================================================================= ! #
# ! ================================================================================= ! #


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


# =========================== #
# UPDATE ALL DEADLINES METHOD #
# =========================== #
def update_all_deadlines():
    """
    It updates all the deadlines of all sources to see on startup the update
    deadline.
    """
    cursor.execute("SELECT id, number_pages, studied_pages, arr_sessions FROM sources;")
    sources = cursor.fetchall()
    for x in sources:
        arr_session_week = ast.literal_eval(x[3])  # Converts string to json
        up_deadline = get_string_date(
            calculate_deadline(
                total_pages=x[1],
                studied_pages=x[2],
                arr_session_week=arr_session_week,
                #
                #  The next line is useless but in the future will be necessary to determine
                #  the type of the source (book, video or audio)
                #
                is_book=True,
            )
        )

        cursor.execute(
            "UPDATE sources SET deadline = ? WHERE id = ?;", (up_deadline, x[0])
        )
        con.commit()


# ! ================================================================================= ! #
# ! ================================================================================= ! #
# ! =============================== FLASHCARD METHODS =============================== ! #
# ! ================================================================================= ! #
# ! ================================================================================= ! #


# =============================== #
# GET FLASHCARDS FOR TABLE METHOD #
# =============================== #
def get_flashcards_for_table(source_id: int) -> list:
    """
    It returns the flashcards of the deck (related to source_id)
    """
    cursor.execute(
        f"SELECT id, front, back, deadline, box FROM flashcards WHERE source_id = {source_id}"
    )
    result = cursor.fetchall()

    return result


# ================================== #
# GET TODAY FLASHCARDS SOURCE METHOD #
# ================================== #
def get_today_flashcards_source(source_id: int) -> list:
    today_str = datetime.now().strftime("%Y-%m-%d")
    query = "SELECT id, front, back, box, source_id FROM flashcards WHERE deadline = ? AND source_id = ? "
    parameters = (today_str, source_id)
    cursor.execute(query, parameters)

    result = cursor.fetchall()

    return result


# ================================ #
# SET SELECTED FLASHCARD ID METHOD #
# ================================ #
def set_selected_flashcard_id(id: int | None):
    global selected_flashcard_id
    selected_flashcard_id = id


# ================================ #
# GET SELECTED FLASHCARD ID METHOD #
# ================================ #
def get_selected_flashcard_id() -> int | None:
    global selected_flashcard_id
    return selected_flashcard_id


# ========================== #
# GET FLASHCARDS LIST METHOD #
# ========================== #
def get_flashcards_list() -> list:
    global flashcards_list
    return flashcards_list


# ======================= #
# APPEND FLASHCARD METHOD #
# ======================= #
def append_flashcard(flashcard: tuple):
    global flashcards_list
    flashcards_list.append(flashcard)


# ======================= #
# REMOVE FLASHCARD METHOD #
# ======================= #
def remove_flashcard(index: int):
    global flashcards_list
    flashcards_list.pop(index)


# =================== #
# SET FLASHCARDS LIST #
# =================== #
def set_flashcards_list(f_list: list):
    global flashcards_list
    flashcards_list = copy.copy(f_list)


# ========================= #
# SET ROW FLASHCARDS METHOD #
# ========================= #
def set_row_flashcards(row: int):
    global row_flashcards
    row_flashcards = row


# ========================= #
# GET ROW FLASHCARDS METHOD #
# ========================= #
def get_row_flashcards() -> int:
    global row_flashcards
    return row_flashcards


# ========================= #
# SAVE NEW FLASHCARD METHOD #
# ========================= #
def save_new_flashcard(front, back, filename):
    text_front = front
    text_back = back
    box = 0
    deadline = datetime.now().strftime("%Y-%m-%d")
    source_id = get_selected_source_id()
    filename_scheme = filename

    cursor.execute(
        "INSERT INTO flashcards(front, back, box, deadline, source_id, filename_scheme) VALUES (?, ?, ?, ?, ?, ?)",
        (text_front, text_back, box, deadline, source_id, filename_scheme),
    )
    con.commit()


# ======================= #
# UPDATE FLASHCARD METHOD #
# ======================= #
def update_flashcard(flashcard_id, front, back):
    """
    It updates the data of a specific flashcard of a specific source.
    """
    cursor.execute(
        "UPDATE flashcards SET front = ?, back = ? WHERE id = ?",
        (front, back, flashcard_id),
    )
    con.commit()


# ! ================================================================================= ! #
# ! ================================================================================= ! #
# ! ================================= LATEX METHODS ================================= ! #
# ! ================================================================================= ! #
# ! ================================================================================= ! #


# =================== #
# RENDER LATEX METHOD #
# =================== #
def render_latex(
    formula: str, fontsize: int = 12, dpi: int = 300, format_: str = "png"
) -> bytes:
    # Create a figure with the specified size and add the LaTeX formula
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, "${}$".format(formula), fontsize=fontsize)

    # Save the figure to a BytesIO buffer
    buffer = BytesIO()
    fig.savefig(
        buffer,
        dpi=dpi,
        transparent=False,
        format=format_,
        bbox_inches="tight",
        pad_inches=0.0,
    )

    # Close the figure and return the image data
    plt.close(fig)
    return buffer.getvalue()
