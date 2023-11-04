import tkinter as tk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

from methods import exists_filename, save_diagram
from setup import cursor


def set_image_label(
    label: tk.Label, filename: str, width_label: int, height_label: int
):
    """
    It changes the image of the label.
    """
    img = Image.open(filename)
    size_image = img.size
    new_width_label = min(width_label, size_image[0])
    new_height_label = min(height_label, size_image[1])

    # To avoid the stretch of the image I take the min
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


def ask_filename() -> str:
    filename = askopenfilename(title="diagram path")
    return filename


def save_new_diagram(
    label: tk.Label, flashcard_id: int, width_label: int, height_label: int
):
    filename = ask_filename()
    set_image_label(label, filename, width_label=width_label, height_label=height_label)
    save_diagram(filename=filename, flashcard_id=flashcard_id)


def view_diagram(flashcard_id: int):
    if flashcard_id is not None:
        cursor.execute(
            "SELECT filename_diagram FROM flashcards WHERE id=?", (flashcard_id,)
        )

        result = cursor.fetchone()
        filename = result[0]

        size_window = 800
        diagram_window = tk.Tk()
        diagram_window.title("Diagram")
        diagram_window.geometry(f"{size_window}x{size_window}")
        diagram_window.minsize(width=size_window, height=size_window)
        diagram_window.resizable(False, False)

        if not exists_filename(filename):
            filename = ask_filename()

        image_width = size_window - 50
        image_height = size_window - 50
        image_label = tk.Label(diagram_window)

        set_image_label(image_label, filename, image_width, image_height)

        image_label.pack()
        tk.Button(
            diagram_window,
            text="Change diagram",
            command=lambda: save_new_diagram(
                label=image_label,
                flashcard_id=flashcard_id,
                width_label=image_width,
                height_label=image_height,
            ),
        ).pack()

        diagram_window.mainloop()
