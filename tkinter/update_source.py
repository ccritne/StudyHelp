import tkinter as tk
from tkinter import ttk
from methods import *
from datetime import datetime as dt
import logging as log

"""
These methods avoid re-enumerating tkinter's grid.
You can create a different layout without losing time changing numbers of rows and columns.
You can swap elements. 
If u want go to new row use next_row; 
if u want put one element next to another use next_column.
"""

# Create log for this script:
log.basicConfig(
    filename="logs/update_source.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)


# ! FUNDAMENTAL METHODS ! #


# =============== #
# NEXT ROW METHOD #
# =============== #
def next_row(row: int, column: int):
    """
    ## `next_row` method

    ====================================

    #### Description

    Moves to the next row in the TkInterface's grid.
    """
    return (
        row + 1,
        column,
    )  # ? modified so it takes the column as input too and not just the value 1, is it ok? (@marco-secci)


# ================== #
# NEXT COLUMN METHOD #
# ================== #
def next_column(row: int, column: int):
    """
    ## `next_column` method

    ====================================

    #### Description

    Moves to the next column in the TkInterface's grid.
    """
    return (row, column + 1)


# ====================== #
# TOGGLE LECTURES METHOD #
# ====================== #
def toggle_lectures(
    checkbox_var: tk.IntVar,
    name_course_entry: tk.Entry,
    name_course_label: tk.Label,
    btn_slots: tk.Button,
    row: int,
    column: int,
):
    """
    ## `toggle_lectures` method

    =====================================

    #### Description:

    If there's a lecture associated with the source, it gives the possibility
    to add a name to the lecture and the corresponding time slots.
    """

    # If the lecture checkbox gets clicked, the lecture's name and timetable appear:
    if checkbox_var.get() == 1:
        # Logging:
        log.info(f"{dt.now()}: Lecture checkbox clicked. ")

        name_course_label.grid(row=row, column=column)
        name_course_entry.grid(row=row, column=column + 1)
        btn_slots.grid(row=row, column=column + 2)
    else:
        name_course_label.grid_remove()
        name_course_entry.grid_remove()
        btn_slots.grid_remove()


# ============= #
# UPDATE SOURCE #
# ============= #
def update_source(command: str = "New"):
    """
    ## `update_source` method

    ===================================

    #### Description

    It lets the user update the source, for example by adding
    a lecture associated with it, or how long it takes to study
    or complete it during a week.
    """
    # Creating main window:
    source_window = tk.Tk()
    source_window.title(f"{command} source")
    source_window.resizable(False, False)

    # Default name of the source (empty):
    default_name = ""

    # Changing the source name when it gets modified:
    if command == "Modify":
        default_name = get_source_values(get_selected_source_id())
        # Logging:
        log.info(f"{dt.now()}: Changed source name into {default_name}. ")

    # Defining default values for row and column:
    row = 1
    column = 1

    # Creating "Name" label:
    name_label = tk.Label(source_window, text="Name")
    name_label.grid(row=row, column=column)

    # Creating an input field (Entry widget):
    row, column = next_column(row, column)
    name_entry = tk.Entry(source_window, width=15)

    # Setting the default value:
    name_entry.insert(0, default_name)
    name_entry.grid(row=row, column=column)

    # Initializing variables:
    with_lectures = True  # ! Replace with your variable
    default_name_course = ""  # ! Replace with your variable

    # * Checkbox creation: * #

    # Checkbox row and column:
    row, column = next_row(row, column)
    row_checkbox_lectures = row + 1
    column_checkbox_lectures = column

    # Checkbox visualization:
    checkbox_var = tk.IntVar()
    checkbox = tk.Checkbutton(
        source_window,
        text="Associate with lectures?",
        variable=checkbox_var,
        command=lambda: toggle_lectures(
            checkbox_var,
            name_course_entry,
            name_course_label,
            btn_slots,
            row_checkbox_lectures,
            column_checkbox_lectures,
        ),
    )
    # Logging:
    log.info(f"{dt.now()}: Created checkbox for lectures. ")

    checkbox.grid(row=row, column=column + 1)

    # Name course label:
    row, column = next_row(row, column)
    name_course_label = tk.Label(source_window, text="Name course:")
    name_course_label.grid(row=row, column=column)

    # Name course entry:
    row, column = next_column(row, column)
    name_course_entry = tk.Entry(source_window, width=15)
    name_course_entry.insert(0, default_name_course)
    name_course_entry.grid(row=row, column=column)

    # Button to insert slots:
    row, column = next_column(row, column)
    btn_slots = tk.Button(
        source_window,
        text="Insert slots",
        state="normal" if with_lectures else "disabled",
    )
    btn_slots.grid(row=row, column=column)

    # Initializing visibility:
    toggle_lectures(
        checkbox_var,
        name_course_entry,
        name_course_label,
        btn_slots,
        row_checkbox_lectures,
        column_checkbox_lectures,
    )

    # Creating the separator:
    row, column = next_row(row, column)
    separator = ttk.Separator(source_window, orient="horizontal")
    separator.grid(row=row, column=column, columnspan=3, sticky="ew")

    # Creating "Day" label:
    row, column = next_row(row, column)
    label_day = tk.Label(source_window, text="Day", width=5, anchor="center")
    label_day.grid(row=row, column=column)

    # Creating "Sessions" label:
    row, column = next_column(row, column)
    label_sessions = tk.Label(source_window, text="Sessions", width=10, anchor="center")
    label_sessions.grid(row=row, column=column)

    # Creating "Minutes left" label:
    row, column = next_column(row, column)
    label_minutes_left = tk.Label(
        source_window, text="Minutes left", width=10, anchor="center"
    )
    label_minutes_left.grid(row=row, column=column)

    study_days = [1, 1, 1, 1, 1, 1, 1]
    sessions = "0000000"

    # Cycling through every day of the week:
    for x in range(7):
        if study_days[x]:
            row, column = next_row(row, column)

            # Calculating the remaining minute of the current day:

            max_study_hour = get_settings_value("max_study_hour")
            total_minutes = get_total_minutes(x)
            remaining_minutes = max_study_hour * 60 - total_minutes

            # Create labels, entry widgets, and text widgets for each day:
            label_day = tk.Label(
                source_window, text=WEEKDAYS[x], width=5, anchor="center"
            )
            label_day.grid(row=row, column=column)

            # TODO Disable Entry if remaining minutes <= 0
            # ! (@marco-secci) I tried to do it this way, it needs to get tested.
            row, column = next_column(row, column)
            try:
                entry_sessions = tk.Entry(source_window, width=10, justify="center")
                entry_sessions.insert(0, sessions[x])
                entry_sessions.grid(row=row, column=column)
            except remaining_minutes <= 0:
                no_minutes_label = tk.Label(
                    source_window, text="No minutes left! ", width=5, anchor="center"
                )
                no_minutes_label.grid(row, column)
                # Logging:
                log.info(
                    f"{dt.now()}: No minutes are left on {WEEKDAYS[x]}. The label 'No minutes left!' has been created instead of the entry for the minutes. "
                )

            row, column = next_column(row, column)
            label_remaining_minutes = tk.Label(
                source_window, text=remaining_minutes, width=10, anchor="center"
            )
            label_remaining_minutes.grid(row=row, column=column)

    # Creating "Insert slots" button:
    row, column = next_row(row, column)
    row, column = next_column(row, column)
    button_insert_slots = tk.Button(source_window, text="Insert slots")
    button_insert_slots.grid(row=row, column=column)
    # Logging:
    log.info(f"{dt.now()}: 'Insert slots' button created.")

    row, column = next_row(row, column)
    separator = ttk.Separator(source_window, orient="horizontal")
    separator.grid(row=row, column=column, columnspan=3, sticky="ew")

    # Creating "Pages" section:
    row, column = next_row(row, column)
    # label:
    label_number_pages = tk.Label(source_window, text="Pages")
    label_number_pages.grid(row=row, column=column)
    # Logging:
    log.info(f"{dt.now()}: Label for 'Pages' created. ")
    # Entry:
    row, column = next_column(row, column)
    entry_number_pages = tk.Entry(source_window, width=4)
    entry_number_pages.grid(row=row, column=column)
    # Logging:
    log.info(f"{dt.now()}: Entry for 'Pages' created. ")

    # Creating "Studied pages" section:
    row, column = next_row(row, column)
    # Label:
    label_studied_pages = tk.Label(source_window, text="Studied pages")
    label_studied_pages.grid(row=row, column=column)
    # Logging:
    log.info(f"{dt.now()}: Label for 'Studied pages' created. ")
    # Entry:
    row, column = next_column(row, column)
    entry_studied_pages = tk.Entry(source_window, width=4)
    entry_studied_pages.grid(row=row, column=column)
    # Logging:
    log.info(f"{dt.now()}: Entry for 'Studied pages' created. ")

    # Creating "Document" section:
    row, column = next_row(row, column)
    # Label:
    label_document = tk.Label(source_window, text="Document")
    label_document.grid(row=row, column=column)
    # Logging:
    log.info(f"{dt.now()}: Label for 'Document' created. ")
    # Entry:
    row, column = next_column(row, column)
    entry_path_source = tk.Entry(source_window, width=15)
    entry_path_source.grid(row=row, column=column)
    # Logging:
    log.info(f"{dt.now()}: Entry for 'Document' created. ")

    # Creating "Browse" button:
    row, column = next_column(row, column)
    button_browse = tk.Button(source_window, text="Browse")
    button_browse.grid(row=row, column=column)
    # Logging:
    log.info(f"{dt.now()}: Button 'Browse' created. ")

    # Creating "Deadline" section:
    row, column = next_row(row, column)
    # Label:
    label_deadline = tk.Label(source_window, text="Deadline", width=20)
    label_deadline.grid(row=row, column=column)
    # Logging:
    log.info(f"{dt.now()}: Label for 'Deadline' created. ")
    # Entry:
    row, column = next_column(row, column)
    entry_preview_deadline = tk.Entry(source_window, width=15, state="readonly")
    entry_preview_deadline.grid(row=row, column=column)
    # Logging:
    log.info(f"{dt.now()}: Entry for 'Deadline' created. ")

    # Creating "Update Source" button:
    row, column = next_row(row, column)
    row, column = next_column(row, column)
    button_update_source = tk.Button(source_window, text="Update source")
    button_update_source.grid(row=row, column=column)
    # Logging:
    log.info(f"{dt.now()}: Button 'Update source' created. ")

    # If the windows gets resized, the layout gets resized too:
    source_window.grid_columnconfigure(1, weight=1)
    source_window.grid_rowconfigure(1, weight=1)

    # Starting the application loop:
    source_window.mainloop()


update_source()
