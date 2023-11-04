import tkinter as tk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
import logging as log
from datetime import datetime as dt
from methods import exists_filename, save_diagram
from setup import cursor

# Create log for this script:
log.basicConfig(
    filename="logs/view_diagram.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)


# ====================== #
# SET IMAGE LABEL METHOD #
# ====================== #
def set_image_label(
    label: tk.Label, filename: str, width_label: int, height_label: int
):
    """
    ## `set_image_label` method

    =================================================

    #### Description

    It changes the image of the label.

    =================================================

    #### Parameters

    #### - `label`: `tk.Label`

    The label object of tkinter.

    #### `filename`: `str`

    The path to the image file.

    #### `width_label`: `int`

    Width dimension of the label object.

    #### `height_label`: `int`

    Height dimension of the label object.
    """

    img = Image.open(filename)
    # Logging:
    log.info(f"{dt.now()}: Image {filename} opened. ")
    size_image = img.size
    new_width_label = min(width_label, size_image[0])
    new_height_label = min(height_label, size_image[1])

    # To avoid the stretch of the image, the script will fetch the min
    # between the width/height of the label and the image's size
    if img.width < img.height:
        # If the height image is greater than its width the
        # image is vertical so I switch width <-> height.
        new_width_label = min(height_label, size_image[1])
        new_height_label = min(width_label, size_image[0])

    resized_image = img.resize((new_width_label, new_height_label))

    diagram_image = ImageTk.PhotoImage(resized_image)
    label.configure(image=diagram_image)
    label.photo = diagram_image


# =================== #
# ASK FILENAME METHOD #
# =================== #
def ask_filename() -> str:
    filename = askopenfilename(title="diagram path")
    return filename


# ================ #
# SAVE NEW DIAGRAM #
# ================ #
def save_new_diagram(
    label: tk.Label, flashcard_id: int, width_label: int, height_label: int
):
    try:
        filename = ask_filename()
        set_image_label(
            label, filename, width_label=width_label, height_label=height_label
        )
        save_diagram(filename=filename, flashcard_id=flashcard_id)
        # Logging:
        log.info(f"{dt.now()}: Saved diagram {filename}. ")
    except Exception as e:
        # Logging:
        log.info(f"{dt.now()}: An error occurred while saving diagram {filename}: {e}")


# =================== #
# VIEW DIAGRAM METHOD #
# =================== #
def view_diagram(flashcard_id: int):
    if flashcard_id is not None:
        try:
            # Looking for the diagram image path:
            cursor.execute(
                "SELECT filename_diagram FROM flashcards WHERE id=?", (flashcard_id,)
            )

            result = cursor.fetchone()
            filename = result[0]
            # Logging:
            log.info(f"{dt.now()}: Trying to open diagram {filename}... ")

            # Creating diagram window:
            size_window = 800
            diagram_window = tk.Tk()
            diagram_window.title("Diagram")
            diagram_window.geometry(f"{size_window}x{size_window}")
            diagram_window.minsize(width=size_window, height=size_window)
            diagram_window.resizable(False, False)

            if not exists_filename(filename):
                # Logging:
                log.info(
                    f"{dt.now()}: File {filename} not found in the flashcard {flashcard_id}. Looking for it now... "
                )
                filename = ask_filename()
            # Logging:
            log.info(f"{dt.now()}: Opened diagram {filename}. ")

            # Creating label for the diagram window:
            image_width = size_window - 50
            image_height = size_window - 50
            image_label = tk.Label(diagram_window)
            set_image_label(image_label, filename, image_width, image_height)

            # Creating "Change Diagram" Button:
            image_label.pack()
            tk.Button(
                diagram_window,
                text="Change Diagram",
                command=lambda: save_new_diagram(
                    label=image_label,
                    flashcard_id=flashcard_id,
                    width_label=image_width,
                    height_label=image_height,
                ),
            ).pack()
            # Logging:
            log.info(f"{dt.now()}: Created 'Change Diagram' button. ")

            diagram_window.mainloop()
        except Exception as e:
            # Logging:
            log.info(
                f"{dt.now()}: An error while displaying diagram {filename} occurred: {e} "
            )
