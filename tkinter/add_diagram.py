from methods import *
from datetime import datetime as dt
import logging as log
import tkinter as tk
from tkinter import filedialog, messagebox


def save_diagram(flashcard_id: int, filename: str):
    """
    ## `save_diagram` method

    ===============================================

    #### Description

    It saves the chosen image (usually, a diagram or framework) on the
    selected flashcard. It returns an exit message, that will be interpreted
    by other methods.

    ===============================================

    #### Parameters

    #### - `flashcard_id`: `int`

    The flashcard where the file will be put into.

    #### - `filename`: `str`

    Path to the file to insert in the flashcard (usually, a diagram or framework).
    """

    exit_message = "EXIT_SUCCESS"

    try:
        # Checking the file existence:
        if exists_filename(filename):
            log.info(
                f"{dt.now()}: The file {filename} exists and will be linked to the flashcard {flashcard_id}. "
            )
            try:
                # Updating the database and committing:
                cursor.execute(
                    "UPDATE flashcards SET filename_scheme=? WHERE id=?",
                    (filename, flashcard_id),
                )
                con.commit()
                log.info(
                    f"{dt.now()}: File {filename} has been linked to flashcard {flashcard_id} successfully. "
                )
            except Exception as e:
                log.info(
                    f"{dt.now()}: An ERROR ({e}) occurred while inserting {filename} into the flashcard {flashcard_id}. "
                )
        else:
            # Showing a popup error message in ca se the file is non-existent:
            messagebox.showerror("ERROR", "The specified path is incorrect!")
            log.info(
                f"{dt.now()}: ERROR: the specified path ({filename}) is incorrect! "
            )

            # Updating exit message:
            exit_message = "PATH_WRONG"
    except sqlite3.Error as e:
        # If there's ane error in the database, show it and log it:
        messagebox.showerror(f"Database Error: {str(e)} ")
        log.info(f"{dt.now()}: A DATABASE ERROR occurred: {str(e)} ")

        # Updating exit message:
        exit_message = "DB_ERROR"
    finally:
        # Regardless of the outcome, return the exit message:
        log.info(f"{dt.now}: Operation completed. Exit message: {exit_message}")
        return exit_message


def update_diagram(flashcard_id: int) -> (str, str):
    """
    ## `update_diagram` method

    ========================================

    #### Description

    Changes the diagram file if needed to.

    #### Parameters

    #### - `flashcard_id`: `int`

    The id of the modified flashcard.
    """
    # Creating the top-level window:
    window = tk.Toplevel()
    window.title("File selector")

    # Making the window modal (retaining focus until closed):
    window.grab_set()
    log.info(f"{dt.now()}: Created top-level window. ")

    # Creating the input field:
    tk.Label(window, text="Please, select a file").grid(row=0, column=0, columnspan=2)
    filename_var = tk.StringVar(window)

    # Creating an 'Entry' field (single-line input):
    filename_entry = tk.Entry(window, textvariable=filename_var)
    filename_entry.grid(row=1, column=0, sticky="ew")

    # * ============================================================= * #
    # * Now, three closures (nested methods) will be defined.         * #
    # * This choice has been made because these three functionalities * #
    # * won't be needed anywhere else, so they do not need global     * #
    # * variables and the code it's easier to maintain.               * #
    # * ============================================================= * #

    # ==================== #
    # BROWSE FILES CLOSURE #
    # ==================== #
    def browse_files():
        filename = filedialog.askopenfile(
            filetypes=(("Image Portable Network Graphics", "*.png"),)
        )
        filename_var.set(filename)

    # Creating the 'Browse' button:
    tk.Button(window, text="Browse", command=browse_files).grid(row=1, column=1)

    # =============== #
    # ON SAVE CLOSURE #
    # =============== #
    def on_save():
        filename = filename_var.get()
        if exists_filename(filename):
            exit_message = save_diagram(flashcard_id, filename)

            # If the save is successful, the modal window can be closed:
            if exit_message == "EXIT_SUCCESS":
                window.destroy()

    # Creating the 'Save' button:
    tk.Button(window, text="Save", command=on_save).grid(row=2, column=1, sticky="e")

    # Making the first column expandable:
    window.columnconfigure(0, weight=1)

    # Wait for the window to be closed before returning:
    window.wait_window()

    # Returning the filename and the correct exit message:
    return filename_var.get(), "EXIT_SUCCESS" if filename_var() else "EXIT_WINDOW"


# Use the function like this:
# filename, exit_message = update_scheme(flashcard_id=123)
