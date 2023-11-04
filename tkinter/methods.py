# Imports
from datetime import date, datetime as dt, time, timedelta as td
import copy
import io
from io import BytesIO
import tkinter as tk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import re
import ast
import textwrap
import base64
import os
import logging as log
from termcolor import colored
from calc_deadline import calculate_deadline

# Global variables:
from setup import *

# Create log for this script:
log.basicConfig(
    filename="logs/methods.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)


# ============== #
# FROM TO METHOD #
# ============== #
def from_to(str_from: str, str_to: str, frame: tk.Frame):
    """
    2023-11-03 12:09 PM @marco-secci: We decided to try to port
    StudyHelp from PySimpleGUI to TkInterface without the use of this
    method.
    """
    pass
    # ? [Closed][@marco-secci][to-see]
    # ? QUESTION:
    #
    # What does this method do? I need to know to port it to tk.
    #
    # ! ANSWER (@ccritne)
    # This method allows to hide the old page and show the new page.
    # `Example:
    # You are in Menù and you want to go in Settings. To do this you have to
    # hide the layout of Menù and show the layout of Settings.`
    # This is an imperative of PySimpleGUI. You can't create or change dynamically a layout
    # (except text or image). The structure of the window cannot change. If u want
    # simulate the effect of the change u have to hide and show the elements.


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


# ================== #
# SAVE diagram METHOD #
# ================== #
def save_diagram(flashcard_id, filename):
    cursor.execute(
        "UPDATE flashcards SET filename_diagram=? WHERE id=?",
        (filename, flashcard_id),
    )
    con.commit()


# ====================== #
# EXISTS FILENAME METHOD #
# ====================== #
def exists_filename(filename):
    if filename in [None, "", "EXIT_WINDOW", "FILE_NOT_FOUND"]:
        return False

    is_file = os.path.isfile(filename)

    return is_file


# ? [Closed][@marco-secci][to-see]
# ? QUESTION:
#
# Why do you return the file path above this question,
# but return just a boolean below this question instead of the image/image path?
#
# ! ANSWER (@ccritne)
# exists_filename and exists_img return boolean.
# is_file is boolean variable. os.path.isfile(filename) return True if the file exists in local :D


# ================= #
# EXISTS IMG METHOD #
# ================= #
def exists_img(img):
    # ? explain pls (@marco-secci)
    if img in [None]:
        return False

    return True


# ======================= #
# CONVERT TO BYTES METHOD #
# ======================= #
def convert_to_bytes(filename: str, resize: dict | None = None) -> bytes:
    try:
        img = Image.open(filename)
        if resize is not None:
            img = img.resize(resize)
        with BytesIO() as bio:
            img.save(bio, format="PNG")
            log.info(f"{dt.now()}: Created the bytes equivalent of {filename}. ")
            del img
            return bio.getvalue()
    except Exception as e:
        log.info(f"{dt.now()}: An unexpected ERROR occurred: {e}")
        return None


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


# ============== #
# FROM TO METHOD #
# ============== #
def from_to(str_from: str, str_to: str, frame: tk.Frame):
    pass  # I don't know what this class should do -M


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
        up_deadline = calculate_deadline(
            total_pages=x[1],
            studied_pages=x[2],
            arr_session_week=arr_session_week,
            #
            #  The next line is useless but in the future will be necessary to determine
            #  the type of the source (book, video or audio)
            #
            is_book=True,
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
    filename_diagram = filename

    cursor.execute(
        "INSERT INTO flashcards(front, back, box, deadline, source_id, filename_diagram) VALUES (?, ?, ?, ?, ?, ?)",
        (text_front, text_back, box, deadline, source_id, filename_diagram),
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
    """
    ## `render_latex` method

    =========================================

    #### Description

    Creates an image of a rendered math formula using `LaTeX`.

    #### Parameters

    #### - `formula`: `str`

    The mathematical expression to render in `LaTeX`.

    #### - `fontsize`: `int = 12`

    Font size for the `LaTeX` image.

    #### - `dpi`: `int = 300`

    Manages the quality of the render; the higher, the better.

    #### - `format`: `str = "png"`

    The extension that the image will be saved as.
    """
    try:
        # Create a figure with the specified size and add the LaTeX formula:
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, "${}$".format(formula), fontsize=fontsize)

        # Save the figure to a BytesIO buffer:
        buffer = BytesIO()
        fig.savefig(
            buffer,
            dpi=dpi,
            transparent=False,
            format=format_,
            bbox_inches="tight",
            pad_inches=0.0,
        )

        # Close the figure and return the image data:
        plt.close(fig)
        log.info(f"{dt.now()}: LaTeX render created successfully. ")
        return buffer.getvalue()

    except Exception as e:
        log.info(f"{dt.now()}: An ERROR in the LaTeX rendering occurred: {e}")
        pass  # ? idk if needed (@marco-secci)


# ============================ #
# FROM TEXT TO ELEMENTS METHOD #
# ============================ #
def from_text_to_elements(text: str, parent_widget):
    elements = []
    normal_string = ""

    x = 0
    while x < len(text):
        if text[x : x + 7] == "[latex]":
            if normal_string:
                wrapped_text = textwrap.fill(normal_string)
                label = tk.Label(parent_widget, text=wrapped_text, justify=tk.LEFT)
            normal_string = ""
            x += 7

        elif text[x : x + 8] == "[/latex]":
            latex_content = normal_string
            normal_string = ""
            image_bytes = render_latex(latex_content)
            image = Image.open(io.BytesIO(image_bytes))
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(parent_widget, image=photo)
            label.image = photo
            elements.append(label)
            x += 8

        else:
            normal_string += text[x]
            x += 1

    if normal_string:
        wrapped_text = textwrap.fill(normal_string)
        label = tk.Label(parent_widget, text=wrapped_text, justify=tk.LEFT)
        elements.append(label)

    return elements


# =============================== #
# ADD LATEX TO INPUT FIELD METHOD #
# =============================== #
def add_latex_to_input_field(window):
    """
    ## `add_latex_to_input_field` method

    ================================================

    #### Description

    It adds [latex][/latex] to string of the selected input field.
    This allows to elaborate an image with the content of text between the tags.

    #### Parameters

    #### `window` TODO
    """

    key = None
    if get_front_input_selected():
        key = "front"

    if get_back_input_selected():
        key = "back"

    if key is not None:
        from tkinter import INSERT

        # Moving the cursor between the tags automatically, to be ready to type and format right away:
        widget = window[key].Widget
        cursor_position = widget.index(INSERT)
        widget.insert(cursor_position, "[latex][/latex]")
        widget.mark_set(INSERT, f"{cursor_position}+7c")


# ! ================================================================================= ! #
# ! ================================================================================= ! #
# ! ========================== DATABASE MANAGEMENT METHODS ========================== ! #
# ! ================================================================================= ! #
# ! ================================================================================= ! #


# ================ #
# CREATE DB METHOD #
# ================ #
def create_db():
    """
    It creates tables inner file 'datas.db' if it is void or some
    tables are deleted.
    """

    try:
        # Query for table of sources
        SQL_SOURCES = """ CREATE TABLE IF NOT EXISTS sources (
                                        id           INTEGER     NOT NULL
                                                                UNIQUE,
                                        course_name   TEXT,
                                        name         TEXT        NOT NULL,
                                        number_pages  INTEGER (5),
                                        studied_pages INTEGER (5),
                                        filename     TEXT,
                                        deadline     TEXT (10),
                                        arr_sessions  TEXT,
                                        insert_date   TEXT (10)   NOT NULL,
                                        PRIMARY KEY (
                                            id AUTOINCREMENT
                                        )
                                    ); """

        cursor.execute(SQL_SOURCES)
        con.commit()

        # Query for table of flashcards
        SQL_FLASHCARDS = """CREATE TABLE IF NOT EXISTS flashcards (
                                        id             INTEGER     PRIMARY KEY AUTOINCREMENT
                                                                NOT NULL,
                                        front          TEXT        NOT NULL,
                                        back           TEXT,
                                        deadline       TEXT (10),
                                        box            INTEGER (2) NOT NULL,
                                        sourceid       INTEGER     NOT NULL,
                                        filename_diagram TEXT
                                    );"""

        cursor.execute(SQL_FLASHCARDS)
        con.commit()

        # Query for table of settings
        SQL_SETTINGS = """CREATE TABLE IF NOT EXISTS settings (
                                        default_hour_notification INTEGER (2) DEFAULT (15) 
                                                                            UNIQUE ON CONFLICT IGNORE,
                                        max_study_hour            INTEGER (2) DEFAULT (8) 
                                                                            UNIQUE ON CONFLICT IGNORE,
                                        study_days               TEXT (7)    DEFAULT [0000000]
                                                                            UNIQUE ON CONFLICT IGNORE,
                                        max_subjects_day          INTEGER (1) DEFAULT (1) 
                                                                            UNIQUE ON CONFLICT IGNORE
                                    );"""

        cursor.execute(SQL_SETTINGS)
        con.commit()

        # Query to insert default value of settings. If the table exists this insert won't be executed
        SQL_SETTINGS_DATA = """INSERT INTO settings(default_hour_notification, max_study_hour, study_days, max_subjects_day) VALUES (15, 8, '0000000', 1);"""

        cursor.execute(SQL_SETTINGS_DATA)
        con.commit()

        # Query for table of calendar
        SQL_CALENDAR = """CREATE TABLE IF NOT EXISTS calendar (
                                        id            INTEGER   NOT NULL,
                                        type          TEXT,
                                        description   TEXT,
                                        inserted_day   TEXT (10) NOT NULL,
                                        date          TEXT (10) NOT NULL,
                                        time_start_date TEXT (5),
                                        time_end_date   TEXT (5),
                                        start_session  INTEGER,
                                        end_session    INTEGER,
                                        source_id      INTEGER,
                                        PRIMARY KEY (
                                            id AUTOINCREMENT
                                        )
                                    );"""

        cursor.execute(SQL_CALENDAR)
        con.commit()
        # Logging:
        log.info(f"{dt.now()}: Successfully created database. ")

    except Exception as e:
        log.info(f"{dt.now()}: There was an ERROR in the creation of the database: {e}")
        pass  # ? idk if needed (@marco-secci)


# ! ================================================================================= ! #
# ! ================================================================================= ! #
# ! =========================== SOURCE MANAGEMENT METHODS =========================== ! #
# ! ================================================================================= ! #
# ! ================================================================================= ! #


# ============================= #
# SET SELECTED SOURCE ID METHOD #
# ============================= #
def set_selected_source_id(id: int | None):
    global selected_source_id
    selected_source_id = id


# ============================= #
# GET SELECTED SOURCE ID METHOD #
# ============================= #
def get_selected_source_id() -> int | None:
    global selected_source_id
    return selected_source_id


# ======================= #
# GET SOURCE VALUE METHOD #
# ======================= #
def get_source_values(source_id: int) -> tuple:
    """
    ## `get_source_values` method

    =======================================

    #### Description

    It gets all values of a specific source.

    #### Parameters

    #### - `source_id`: `int`

    The id of the source to fetch values from.
    """
    cursor.execute("SELECT * FROM sources WHERE id=?", (source_id,))

    return cursor.fetchone()


# ======================= #
# SET SOURCES LIST METHOD #
# ======================= #
def set_sources_list(b_list: list):
    global sources_list
    sources_list = copy.copy(b_list)


# ======================= #
# GET SOURCES LIST METHOD #
# ======================= #
def get_sources_list() -> list:
    global sources_list
    return sources_list


# ====================== #
# SET ROW SOURCES METHOD #
# ====================== #
def set_row_sources(row: int):
    global row_sources
    row_sources = row


# ====================== #
# GET ROW SOURCES METHOD #
# ====================== #
def get_row_sources() -> int:
    global row_sources
    return row_sources


# ======================== #
# ALL SOURCES NAMES METHOD #
# ======================== #
def all_sources_names() -> list:
    """
    ## `all_sources_names` method

    =======================================

    #### Description

    Returns all IDs and names of sources.
    """
    cursor.execute("SELECT id, name FROM sources")
    result = cursor.fetchall()

    return result


# ! ================================================================================= ! #
# ! ================================================================================= ! #
# ! ================================== INPUT METHODS ================================ ! #
# ! ================================================================================= ! #
# ! ================================================================================= ! #


# =================== #
# CHECK STR INT INPUT #
# =================== #
def check_str_int_input(str) -> bool:
    """
    ## `check_str_int_input` method

    =======================================

    #### Description

    Checks wether the input sent is a `str` or an `int`.

    #### Parameters

    #### - `str`: `int` or `str`
    The input.
    """
    regexp = re.compile("[^0-9]")
    if regexp.search(str) or len(str) == 0:
        return False

    return True


# =============================== #
# SET FRONT INPUT SELECTED METHOD #
# =============================== #
def set_front_input_selected(value: bool):
    global front_input_selected
    front_input_selected = value


# =============================== #
# GET FRONT INPUT SELECTED METHOD #
# =============================== #
def get_front_input_selected() -> bool:
    global front_input_selected
    return front_input_selected


# ============================== #
# SET BACK INPUT SELECTED METHOD #
# ============================== #
def set_back_input_selected(value: bool):
    global back_input_selected
    back_input_selected = value


# ============================== #
# GET BACK INPUT SELECTED METHOD #
# ============================== #
def get_back_input_selected() -> bool | None:
    global back_input_selected
    return back_input_selected


# ======================== #
# CHECK INPUT CLICK METHOD #
# ======================== #
def check_input_click(event):
    """
    ## `check_input_click` method

    ========================================

    #### Description

    Check if the click happened i the inner, front or back section of input_text.

    #### Parameters

    #### - `event`
    Tracks what type of click has been executed.
    """

    if event == "front_LClick":
        set_back_input_selected(False)
        set_front_input_selected(True)

    elif event == "back_LClick" or event == "front_Tab":
        # If I click in back or if I press Tab when I am on the front input_text
        set_front_input_selected(False)
        set_back_input_selected(True)


# ! ================================================================================= ! #
# ! ================================================================================= ! #
# ! =========================== TABLES MANAGEMENT METHODS =========================== ! #
# ! ================================================================================= ! #
# ! ================================================================================= ! #


# ===================== #
# SET TABLE DECK METHOD #
# ===================== #
def set_table_deck(tDeck: list):
    global table_deck
    table_deck = copy.copy(tDeck)


# ===================== #
# GET TABLE DECK METHOD #
# ===================== #
def get_table_deck() -> list:
    global table_deck
    return table_deck


# ! ================================================================================= ! #
# ! ================================================================================= ! #
# ! =============================== TIME/DATE METHODS =============================== ! #
# ! ================================================================================= ! #
# ! ================================================================================= ! #


# ======================== #
# GET TOTAL MINUTES METHOD #
# ======================== #
def get_total_minutes(index_day, except_id=None):
    query = "SELECT arr_sessions FROM sources "

    if except_id is not None:
        query = query + " WHERE id <> " + str(except_id)

    cursor.execute(query)
    result = cursor.fetchall()
    total_minutes = 0
    for x in result:
        json = ast.literal_eval(x[0])
        if (
            json[WEEKDAYS[index_day]]["is_study_day"]
            and json[WEEKDAYS[index_day]]["are_there_sessions"]
        ):
            total_minutes += json[WEEKDAYS[index_day]]["total_duration"]
        if json["with_lectures"] and json[WEEKDAYS[index_day]]["are_there_lectures"]:
            total_minutes += json[WEEKDAYS[index_day]]["time_lectures"][
                "duration_lecture"
            ]

    return total_minutes


# ======================== #
# SET SELECTED DATE METHOD #
# ======================== #
def set_selected_date(date: datetime):
    global selected_date
    selected_date = copy.copy(date)


# ======================== #
# GET SELECTED DATE METHOD #
# ======================== #
def get_selected_date() -> datetime | None:
    global selected_date
    return selected_date


# ====================== #
# GET STRING DATE METHOD #
# ====================== #
def get_string_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


# ================================ #
# GET STRING DATE WITH TIME METHOD #
# ================================ #
def get_string_date_with_time(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M")


# ! ================================================================================= ! #
# ! ================================================================================= ! #
# ! ================================= LAYOUT METHODS ================================ ! #
# ! ================================================================================= ! #
# ! ================================================================================= ! #


# ======================= #
# SET FRONT LAYOUT METHOD #
# ======================= #
def set_front_layout(front_ly: list):
    global front_layout
    front_layout = copy.deepcopy(front_ly)


# ====================== #
# SET BACK LAYOUT METHOD #
# ====================== #
def set_back_layout(back_ly: list):
    global back_layout
    back_layout = copy.deepcopy(back_ly)


# ======================= #
# GET FRONT LAYOUT METHOD #
# ======================= #
def get_front_layout() -> list:
    global front_layout
    return front_layout


# ====================== #
# GET BACK LAYOUT METHOD #
# ====================== #
def get_back_layout() -> list:
    global back_layout
    return back_layout
