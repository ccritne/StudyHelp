from setup import *
from datetime import date, datetime, time, timedelta
import copy
from io import BytesIO
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from PIL import Image
import re
import ast
import textwrap
import base64
import os
from tkinter import *


def change_previous_page(old_page: str):
    global previous_page
    previous_page = old_page


def get_previous_page() -> str:
    global previous_page
    return previous_page


def change_actual_page(new_page: str):
    global actual_page
    actual_page = new_page


def get_actual_page() -> str:
    global actual_page
    return actual_page


# from to what? -M
def from_to(str_from: str, str_to: str, window: sg.Window):
    window[str_from].update(visible=False)
    window[str_to].update(visible=True)
    change_previous_page(str_from)
    change_actual_page(str_to)


def calculate_deadline(
    arr_session_week: list,
    is_book: bool = True,
    total_pages: int | None = 0,
    studied_pages: int | None = 0,
) -> datetime:
    today_date = datetime.now()
    today_index = today_date.weekday()

    deadline: datetime = copy.copy(today_date)
    remaining = 0

    index_str = ""

    if is_book:
        remaining = total_pages - studied_pages
        index_str = "total_pages"

    days_to_add = 0

    while today_index < 7:
        if (
            arr_session_week[WEEKDAYS[today_index]]["is_study_day"]
            and arr_session_week[WEEKDAYS[today_index]]["are_there_sessions"]
        ):
            remaining -= min(
                arr_session_week[WEEKDAYS[today_index]][index_str], remaining
            )

        today_index += 1
        if remaining > 0:
            days_to_add += 1

    deadline += timedelta(days=days_to_add)

    week_do = arr_session_week[index_str]

    weeks_add = int(remaining / week_do)

    if weeks_add > 0:
        weeks_add -= 1

    days_add = weeks_add * 7
    remaining -= week_do * weeks_add
    deadline += timedelta(days=days_add)

    today_index = 0

    days_to_add = 0
    while remaining > 0:
        if (
            arr_session_week[WEEKDAYS[today_index]]["is_study_day"]
            and arr_session_week[WEEKDAYS[today_index]]["are_there_sessions"]
        ):
            remaining -= min(
                arr_session_week[WEEKDAYS[today_index]][index_str], remaining
            )

        if today_index < 6:
            today_index += 1
        else:
            today_index = 0

        if remaining > 0:
            days_to_add += 1

    deadline += timedelta(days=days_to_add)

    return deadline


def all_sources_names() -> list:
    cursor.execute("SELECT DISTINCT id, name FROM sources")
    result = cursor.fetchall()

    return result


def get_flashcards_for_table(source_ID: int) -> list:
    cursor.execute(
        f"SELECT ID, front, back, deadline, box FROM flashcards WHERE source_ID = {source_ID}"
    )
    result = cursor.fetchall()

    return result


def get_today_flashcards_source(source_ID: int) -> list:
    today_str = datetime.now().strftime("%Y-%m-%d")
    query = "SELECT ID, front, back, box, source_ID FROM flashcards WHERE deadline = ? AND source_ID = ? "
    parameters = (today_str, source_ID)
    cursor.execute(query, parameters)

    result = cursor.fetchall()

    return result


def get_info_decks() -> list:
    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        f"""SELECT sources.ID,
                                sources.name,
                                flashcards.deadline
                            FROM flashcards
                                LEFT JOIN
                                sources ON flashcards.source_ID = sources.ID
                            ORDER BY sources.ID;
                        """
    )

    array = cursor.fetchall()
    if array != []:
        id = array[0][0]
        table_info = [[id, array[0][1], 0]]
        index = 0
        for x in range(len(array)):
            if array[x][0] != id:  # Sort fetch
                id = array[x][0]
                table_info.append([id, array[x][1], 0])
                index += 1

            if array[x][2] == today_str:
                table_info[index][2] += 1

        return table_info

    return [[]]


def get_settings_value(value: str) -> str | int:
    cursor.execute("SELECT " + value + " FROM settings")

    return cursor.fetchone()[0]


def render_latex(
    formula: str, fontsize: int = 12, dpi: int = 300, format_: str = "png"
) -> bytes:
    # Create a figure with the specified size and add the LaTeX formula
    fig, ax = plt.subplots(figsize=(0.01, 0.01))
    ax.text(0, 0, "${}$".format(formula), fontsize=fontsize)

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


def set_selected_source_ID(id: int | None):
    global selected_source_ID
    selected_source_ID = id


def get_selected_source_ID() -> int | None:
    global selected_source_ID
    return selected_source_ID


def set_selected_flashcard_ID(id: int | None):
    global selected_flashcard_ID
    selected_flashcard_ID = id


def get_selected_flashcard_ID() -> int | None:
    global selected_flashcard_ID
    return selected_flashcard_ID


def convert_to_bytes(filename, resize=None) -> bytes:
    try:
        img = Image.open(filename)
        if resize is not None:
            img = img.resize(resize)
        with BytesIO() as bio:
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
    except:
        return None


def get_source_values(source_ID: int) -> tuple:
    cursor.execute(f"SELECT * FROM sources WHERE ID={source_ID}")

    return cursor.fetchone()


def get_flashcards_array() -> list:
    global flashcards_array
    return flashcards_array


def append_flashcard(flashcard: tuple):
    global flashcards_array
    flashcards_array.append(flashcard)


def remove_flashcard(index: int):
    global flashcards_array
    flashcards_array.pop(index)


def set_flashcards_array(f_array: list):
    global flashcards_array
    flashcards_array = copy.copy(f_array)


def check_str_int_input(str) -> bool:
    regexp = re.compile("[^0-9]")
    if regexp.search(str) or len(str) == 0:
        return False

    return True


def set_sources_array(b_array: list):
    global sources_array
    sources_array = copy.copy(b_array)


def get_sources_array() -> list:
    global sources_array
    return sources_array


def set_table_deck(tDeck: list):
    global table_deck
    table_deck = copy.copy(tDeck)


def get_table_deck() -> list:
    global table_deck
    return table_deck


def get_total_minutes(index_day, except_ID=None):
    query = "SELECT arrSessions FROM sources "

    if except_ID is not None:
        query = query + " WHERE ID <> " + str(except_ID)

    cursor.execute(query)
    result = cursor.fetchall()
    total_minutes = 0
    for x in result:
        json = ast.literal_eval(x[0])
        if (
            json[WEEKDAYS[index_day]]["is_study_day"]
            and json[WEEKDAYS[index_day]]["are_there_sessions"]
        ):
            total_minutes += json[WEEKDAYS[index_day]]["totalDuration"]
        if json["withLectures"] and json[WEEKDAYS[index_day]]["areThereLectures"]:
            total_minutes += json[WEEKDAYS[index_day]]["timeLectures"][
                "durationLecture"
            ]

    return total_minutes


def set_row_sources(row: int):
    global row_sources
    row_sources = row


def get_row_sources() -> int:
    global row_sources
    return row_sources


def set_row_flashcards(row: int):
    global row_flashcards
    row_flashcards = row


def get_row_flashcards() -> int:
    global row_flashcards
    return row_flashcards


def set_front_input_selected(value: bool):
    global front_input_selected
    front_input_selected = value


def get_front_input_selected() -> bool:
    global front_input_selected
    return front_input_selected


def set_back_input_selected(value: bool):
    global back_input_selected
    back_input_selected = value


def get_back_input_selected() -> bool | None:
    global back_input_selected
    return back_input_selected


def set_selected_date(date: datetime):
    global selected_date
    selected_date = copy.copy(date)


def get_selected_date() -> datetime | None:
    global selected_date
    return selected_date


def get_string_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def get_string_date_with_time(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M")


def set_front_layout(front_ly: list):
    global front_layout
    front_layout = copy.deepcopy(front_ly)


def set_back_layout(back_ly: list):
    global back_layout
    back_layout = copy.deepcopy(back_ly)


def get_front_layout() -> list:
    global front_layout
    return front_layout


def get_back_layout() -> list:
    global back_layout
    return back_layout


def from_text_to_elements(text: str):
    elements = []
    normal_string = ""

    x = 0
    while x < len(text):
        if text[x : x + 7] == "[latex]":
            if normal_string:
                elements.append(
                    [sg.Text(text=textwrap.fill(normal_string), expand_x=True)]
                )
            normal_string = ""
            x += 7

        elif text[x : x + 8] == "[/latex]":
            if normal_string:
                elements.append(
                    [sg.Text(text=textwrap.fill(normal_string), expand_x=True)]
                )
            normal_string = ""
            latex_content = text[x - 7 : x]
            image_bytes = render_latex(latex_content)
            image_base64 = base64.b64encode(image_bytes)
            elements.append([sg.Column([[sg.Image(data=image_base64)]])])
            x += 8

        else:
            normal_string += text[x]
            x += 1

    if normal_string:
        elements.append([sg.Text(text=textwrap.fill(normal_string), expand_x=True)])

    return elements


def from_number_to_time(number: int) -> str:
    if number < 10:
        return "0" + str(number)

    return str(number)


def exists_filename(filename):
    if filename in [None, "", "EXIT_WINDOW", "FILE_NOT_FOUND"]:
        return False

    is_file = os.path.is_file(filename)

    return is_file


def exists_img(img):
    if img in [None]:
        return False

    return True


def check_input_click(event):
    if event == "frontInput_LClick":
        set_back_input_selected(False)
        set_front_input_selected(True)

    if event == "backInput_LClick" or event == "frontInput_Tab":
        set_front_input_selected(False)
        set_back_input_selected(True)


def add_latex_to_input_field(window):
    key = None
    if get_front_input_selected():
        key = "front"

    if get_back_input_selected():
        key = "back"

    if key is not None:
        widget = window[key].Widget
        cursor_position = widget.index(INSERT)
        widget.insert(cursor_position, "[latex][/latex]")
        widget.mark_set(INSERT, f"{cursor_position}+7c")


def save_new_flashcard(front, back, filename):
    text_front = front
    text_back = back
    box = 0
    deadline = datetime.now().strftime("%Y-%m-%d")
    source_ID = get_selected_source_ID()
    filename_scheme = filename

    query = "INSERT INTO flashcards(front, back, box, deadline, source_ID, filename_scheme) VALUES (?, ?, ?, ?, ?, ?)"

    parameters = (text_front, text_back, box, deadline, source_ID, filename_scheme)

    cursor.execute(query, parameters)
    con.commit()


def update_flashcard(flashcard_ID, front, back):
    query = "UPDATE flashcards SET front = ?, back = ? WHERE ID = ?"

    parameters = (front, back, flashcard_ID)

    cursor.execute(query, parameters)
    con.commit()
