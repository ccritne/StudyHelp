import tkinter as tk
from tkinter import Toplevel, Label, Scrollbar, Canvas
from tk_methods import from_text_to_elements
import logging as log
from datetime import datetime as dt

# Create log for this script:
log.basicConfig(
    filename="logs/preview.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)


# =================== #
# PREVIEW CARD METHOD #
# =================== #
def preview_flashcard(text_front: str, text_back: str):
    """
    ## `preview_flashcard` method

    ======================================

    #### Description

    It previews the flashcard into a new window.

    #### Parameters

    #### - `text_front`: `str`

    The text typed on the front of the flashcard
    (usually, the question).

    #### - `text_back`: `str`

    The text typed on the back of the flashcard
    (usually, the answer to the question on the front).
    """

    # Creating the top-level window:
    preview_window = Toplevel()
    preview_window.title("Preview Flashcard")
    # Logging:
    log.info(
        f"{dt.now()}: Created top-level window for the flashcard; expected front text: {front_text} - expected back text: {back_text}"
    )

    # Creating canvas e scrollbar for the front-text window:
    canvas_front = Canvas(preview_window)
    scrollbar_front = Scrollbar(preview_window, command=canvas_front.yview)
    canvas_front.configure(yscrollcommand=scrollbar_front.set)
    # Logging:
    log.info(f"{dt.now()}: Created Canvas and scrollbar for the front text window. ")

    # Creating the frame for the front elements:
    frame_front = tk.Frame(canvas_front)
    canvas_front.create_window((0, 0), window=frame_front, anchor="nw")
    # Logging:
    log.info(f"{dt.now()}: Created frame for front elements. ")

    # Adding front label and content:
    label_front = Label(frame_front, text="Front: ", font=("Arial", 16))
    label_front.pack(fill="x", padx=5, pady=5)
    # Logging:
    log.info(f"{dt.now()}: Created front label. ")

    # Rendering the front elements in LaTeX format:
    elements_front = from_text_to_elements(text_front, frame_front)
    for element in elements_front:
        element.pack(fill="x", padx=5, pady=5)
    # Logging:
    log.info(f"{dt.now()}: Rendered LaTeX for the front elements. ")

    # Re-doing the same process for the back elements:
    # Canvas and scrollbar:
    canvas_back = Canvas(preview_window)
    scrollbar_back = Scrollbar(preview_window, command=canvas_back.yview)
    canvas_back.configure(yscrollcommand=scrollbar_back.set)
    # Logging:
    log.info(f"{dt.now()}: Created Canvas and scrollbar for the back text window. ")

    # Frame:
    frame_back = tk.Frame(canvas_back)
    canvas_back.create_window((0, 0), window=frame_back, anchor="nw")
    # Logging:
    log.info(f"{dt.now()}: Created frame for back elements. ")

    # Label and content:
    label_back = Label(frame_back, text="Back:", font=("Arial", 16))
    label_back.pack(fill="x", padx=5, pady=5)
    # Logging:
    log.info(f"{dt.now()}: Created back label. ")

    # LaTeX formatting:
    elements_back = from_text_to_elements(text_back, frame_back)
    for element in elements_back:
        element.pack(fill="x", padx=5, pady=5)
    # Logging:
    log.info(f"{dt.now()}: Rendered LaTeX for the back elements. ")

    # Packing everything into the window:
    # Front:
    label_front.pack(side="top", fill="x")
    canvas_front.pack(side="top", fill="both", expand=True)
    scrollbar_front.pack(side="right", fill="y")
    # Logging:
    log.info(f"{dt.now()}: Packed everything on the front window. ")

    # Back:
    label_back.pack(side="top", fill="x")
    canvas_back.pack(side="top", fill="both", expand=True)
    scrollbar_back.pack(side="right", fill="y")
    # Logging:
    log.info(f"{dt.now()}: Packed everything on the back window. ")

    # Updating the scrollable region after adding all elements:
    # Front:
    frame_front.update_idletasks()
    canvas_front.config(scrollregion=canvas_front.bbox("all"))
    # Logging:
    log.info(f"{dt.now()}: Updated scrollable region for the front. ")

    # Back:
    frame_back.update_idletasks()
    canvas_back.config(scrollregion=canvas_back.bbox("all"))
    # Logging:
    log.info(f"{dt.now()}: Updated scrollable region for the back. ")

    # Making the window modal - it retains focus until closed:
    preview_window.transient(preview_window.master)
    preview_window.grab_set()
    preview_window.wait_window()
    # Logging:
    log.info(f"{dt.now()}: The flashcard preview window is now modal. ")


# ! Example main - it will run only when this file is executed:

if __name__ == "__main__":
    # Replace this with the actual text you want to display:
    front_text = r"This is the front text with [latex]LaTeX content[/latex]."
    back_text = r"This is the back text with [latex]\frac{a}{b}[/latex]. "

    # Call the preview_card function with the example texts:
    preview_flashcard(front_text, back_text)
