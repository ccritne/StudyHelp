import tkinter as tk
from tkinter import ttk
from methods import *


def nextRow(row: int, column: int):
    return (row + 1, 1)


"""
These methods allows to avoid the re-enumerate the grid of tkinter.
You can create a different layout without lost time to change number of row and column.
You can swap elements. 
If u want go to new row use nextRow instead if u want put one element next to other use nextColumn.
"""


def nextColumn(row: int, column: int):
    return (row, column + 1)


def toggle_lectures(
    checkbox_var: tk.IntVar,
    name_course_entry: tk.Entry,
    name_course_label: tk.Label,
    btn_slots: tk.Button,
    row: int,
    column: int,
):
    if checkbox_var.get() == 1:
        name_course_label.grid(row=row, column=column)
        name_course_entry.grid(row=row, column=column + 1)
        btn_slots.grid(row=row, column=column + 2)
    else:
        name_course_label.grid_remove()
        name_course_entry.grid_remove()
        btn_slots.grid_remove()


def update_source(command: str = "New"):
    source_window = tk.Tk()
    source_window.title(f"{command} source")
    source_window.resizable(False, False)

    # Default name of the source
    default_name = ""

    if command == "Modify":
        default_name = get_source_values(get_selected_source_id())

    row = 1
    column = 1
    # Create a label
    name_label = tk.Label(source_window, text="Name")
    name_label.grid(row=row, column=column)

    row, column = nextColumn(row, column)

    # Create an input field (Entry widget)
    name_entry = tk.Entry(source_window, width=15)
    name_entry.insert(0, default_name)  # Set the default value
    name_entry.grid(row=row, column=column)

    # Initialize variables
    with_lectures = True  # Replace with your variable
    default_name_course = ""  # Replace with your variable

    row, column = nextRow(row, column)
    # Checkbox

    row_checkbox_lectures = row + 1
    column_checkbox_lectures = column

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
    checkbox.grid(row=row, column=column + 1)

    row, column = nextRow(row, column)

    # Name course label
    name_course_label = tk.Label(source_window, text="Name course:")
    name_course_label.grid(row=row, column=column)

    row, column = nextColumn(row, column)

    # Name course entry
    name_course_entry = tk.Entry(source_window, width=15)
    name_course_entry.insert(0, default_name_course)
    name_course_entry.grid(row=row, column=column)

    row, column = nextColumn(row, column)

    # Button to insert slots
    btn_slots = tk.Button(
        source_window,
        text="Insert slots",
        state="normal" if with_lectures else "disabled",
    )
    btn_slots.grid(row=row, column=column)

    # Initialize visibility
    toggle_lectures(
        checkbox_var,
        name_course_entry,
        name_course_label,
        btn_slots,
        row_checkbox_lectures,
        column_checkbox_lectures,
    )

    row, column = nextRow(row, column)
    separator = ttk.Separator(source_window, orient="horizontal")
    separator.grid(row=row, column=column, columnspan=3, sticky="ew")

    row, column = nextRow(row, column)
    # Create labels for "Day", "Sessions", and "Minutes left"
    label_day = tk.Label(source_window, text="Day", width=5, anchor="center")
    label_day.grid(row=row, column=column)

    row, column = nextColumn(row, column)

    label_sessions = tk.Label(source_window, text="Sessions", width=10, anchor="center")
    label_sessions.grid(row=row, column=column)

    row, column = nextColumn(row, column)

    label_minutes_left = tk.Label(
        source_window, text="Minutes left", width=10, anchor="center"
    )
    label_minutes_left.grid(row=row, column=column)

    study_days = [1, 1, 1, 1, 1, 1, 1]
    sessions = "0000000"

    for x in range(7):
        if study_days[x]:
            row, column = nextRow(row, column)

            # Calculate of the remaining minutes in this day.
            # TODO Disable Entry if remaining minutes <= 0
            max_study_hour = get_settings_value("max_study_hour")
            total_minutes = get_total_minutes(x)
            remaining_minutes = max_study_hour * 60 - total_minutes

            # Create labels, entry widgets, and text widgets for each day
            label_day = tk.Label(
                source_window, text=WEEKDAYS[x], width=5, anchor="center"
            )
            label_day.grid(row=row, column=column)

            row, column = nextColumn(row, column)

            entry_sessions = tk.Entry(source_window, width=10, justify="center")
            entry_sessions.insert(0, sessions[x])
            entry_sessions.grid(row=row, column=column)

            row, column = nextColumn(row, column)

            label_remaining_minutes = tk.Label(
                source_window, text=remaining_minutes, width=10, anchor="center"
            )
            label_remaining_minutes.grid(row=row, column=column)

    row, column = nextRow(row, column)
    row, column = nextColumn(row, column)

    button_insert_slots = tk.Button(source_window, text="Insert slots")
    button_insert_slots.grid(row=row, column=column)

    row, column = nextRow(row, column)

    separator = ttk.Separator(source_window, orient="horizontal")
    separator.grid(row=row, column=column, columnspan=3, sticky="ew")

    row, column = nextRow(row, column)

    # Create and configure widgets
    label_number_pages = tk.Label(source_window, text="Pages")
    label_number_pages.grid(row=row, column=column)

    row, column = nextColumn(row, column)

    entry_number_pages = tk.Entry(source_window, width=4)
    entry_number_pages.grid(row=row, column=column)

    row, column = nextRow(row, column)

    label_studied_pages = tk.Label(source_window, text="Done pages")
    label_studied_pages.grid(row=row, column=column)

    row, column = nextColumn(row, column)

    entry_studied_pages = tk.Entry(source_window, width=4)
    entry_studied_pages.grid(row=row, column=column)

    row, column = nextRow(row, column)

    label_document = tk.Label(source_window, text="Document")
    label_document.grid(row=row, column=column)

    row, column = nextColumn(row, column)

    entry_path_source = tk.Entry(source_window, width=15)
    entry_path_source.grid(row=row, column=column)

    row, column = nextColumn(row, column)

    button_browse = tk.Button(source_window, text="Browse")
    button_browse.grid(row=row, column=column)

    row, column = nextRow(row, column)

    label_deadline = tk.Label(source_window, text="Deadline", width=20)
    label_deadline.grid(row=row, column=column)

    row, column = nextColumn(row, column)

    entry_preview_deadline = tk.Entry(source_window, width=15, state="readonly")
    entry_preview_deadline.grid(row=row, column=column)

    row, column = nextRow(row, column)
    row, column = nextColumn(row, column)

    button_update_source = tk.Button(source_window, text="Update Source")
    button_update_source.grid(row=row, column=column)

    source_window.mainloop()


update_source()
