import tkinter as tk
from tkinter import filedialog
from methods import *
from preview import preview_flashcard
from datetime import datetime as dt
import logging as log

# Create log for this script:
log.basicConfig(
    filename="logs/add_card.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)


# ======================= #
# CREATE FLASHCARD METHOD #
# ======================= #
def create_flashcard():
    """
    ## `create_flashcard` method

    =========================================

    #### Description
    TODO
    """
    # Logging:
    log.info(f"{dt.now()}: Flashcard creating window opened.")

    # Creating the main window:
    root = tk.Tk()
    root.title("Add new flashcard ")

    # Creating the front-input window:
    tk.Label(root, text="Front").grid(row=0, column=0)
    # Constructing 'Entry' widget (single-line input):
    front_entry = tk.Entry(root)
    front_entry.grid(row=0, column=1, sticky="ew")

    # Creating the back-input window:
    tk.Label(root, text="Back").grid(row=1, column=0)
    # Constructing 'Text' widget (multi-line input):
    back_entry = tk.Text(root, height=8)
    back_entry.grid(row=1, column=1, sticky="ew")

    # defining document input:
    tk.Label(root, text="Document").grid(row=2, column=0)
    filename_entry = tk.Entry(root)
    filename_entry.grid(row=2, column=1, sticky="ew")

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
        """
        ## `browse_files` closure

        =========================================

        #### Description

        This is a closure of the `create_flashcard()` method, meaning a nested method.

        It describes the behaviour of the "Browse" button used to choose a file for a
        flashcard.
        """
        # Logging:
        log.info(f"{dt.now()}: Using closure 'browse_files'... ")

        # Creating the window to browse files:
        filename = filedialog.askopenfile(
            filetypes=(("Image Portable Network Graphics", "*.png"),)
        )
        # Putting the path of the chosen file in the Entry widget:
        filename_entry.delete(0, tk.END)
        filename_entry.insert(0, filename)

    # Creating 'Browse' button:
    tk.Button(root, text="Browse", command=browse_files).grid(row=2, column=2)

    # =============== #
    # ON SAVE CLOSURE #
    # =============== #
    def on_save():
        """
        ## `on_save` closure

        =========================================

        #### Description

        This is a closure of the `create_flashcard()` method, meaning a nested method.

        It describes the behaviour of the "Save" button used to save the file selection
         for a flashcard.
        """
        # Logging:
        log.info(f"{dt.now()}: Using closure 'on_save'... ")
        save_new_flashcard(
            front=front_entry.get(),
            back=back_entry.get("1.0", tk.END),
            filename=filename_entry.get(),
        )
        root.destroy()

    # ================== #
    # ON PREVIEW CLOSURE #
    # ================== #
    def on_preview():
        """
        ## `on_preview` closure

        =========================================

        #### Description

        This is a closure of the `create_flashcard()` method, meaning a nested method.

        It describes the behaviour of the "Preview" button used to save the file selection
         for a flashcard.
        """
        preview_flashcard(
            front=front_entry.get(),
            back=back_entry.get("1.0", tk.END),
        )

    # Creating buttons:
    tk.Button(root, text="Save", command=on_save).grid(row=3, column=1, sticky="ew")
    tk.Button(root, text="Preview", command=on_preview).grid(
        row=3, column=2, sticky="ew"
    )
    # Logging:
    log.info(f"{dt.now()}: Button 'Save' and 'Preview created. ")

    # If the windows gets resized, the layout gets resized too:
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(1, weight=1)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    # Call the add_card function
    create_flashcard()
