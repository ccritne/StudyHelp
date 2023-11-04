import tkinter as tk
from tkinter import Toplevel
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

from functions import exists_filename, save_diagram
from setup import cursor


def set_image_label(label: tk.Label, filename: str):
    label.update_idletasks()
    img = Image.open(filename)
    resized_img = img.resize((label.winfo_width(), label.winfo_height()))
    diagram_image = ImageTk.PhotoImage(resized_img)
    label.configure(image=diagram_image)
    label.photo_ref = diagram_image


def ask_filename() -> str:
    filename = askopenfilename(title="diagram path")
    return filename


def save_new_diagram(label: tk.Label, flashcard_id: int):
    filename = ask_filename()
    set_image_label(label, filename)
    save_diagram(filename=filename, flashcard_id=flashcard_id)


def view_diagram(flashcard_id: int):
    if flashcard_id is not None:
        cursor.execute(
            "SELECT filename_diagram FROM flashcards WHERE id=?", (flashcard_id,)
        )

        result = cursor.fetchone()
        filename = result[0]

        diagram_window = tk.Tk()
        diagram_window.title("Diagram")
        diagram_window.geometry("800x550")

        if not exists_filename(filename):
            filename = ask_filename()

        image_label = tk.Label(
            diagram_window,
            width=800,
            height=500,
        )

        image_label.pack()

        set_image_label(image_label, filename)

        tk.Button(
            diagram_window,
            text="Change diagram",
            command=lambda: save_new_diagram(
                label=image_label, flashcard_id=flashcard_id
            ),
        ).pack()

        diagram_window.mainloop()


view_diagram(50)
