import tkinter as tk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

from functions import exists_filename, save_scheme
from setup import cursor


def set_image_label(label: tk.Label, filename: str):
    label.update_idletasks()
    img = Image.open(filename)
    resized_img = img.resize((label.winfo_width(), label.winfo_height()))
    scheme_image = ImageTk.PhotoImage(resized_img)
    label.configure(image=scheme_image)
    label.image_ref = scheme_image


def ask_filename() -> str:
    filename = askopenfilename(title="Scheme path")
    return filename


def save_new_scheme(label: tk.Label, flashcard_id: int):
    filename = ask_filename()
    set_image_label(label, filename)
    save_scheme(filename=filename, flashcard_id=flashcard_id)


def view_scheme(flashcard_id: int):
    if flashcard_id is not None:
        cursor.execute(
            "SELECT filename_scheme FROM flashcards WHERE id=?", (flashcard_id,)
        )

        result = cursor.fetchone()
        filename = result[0]

        root = tk.Tk()
        root.title("Scheme")
        root.geometry("800x550")

        image_label = tk.Label(root, width=800, height=500)
        image_label.pack()

        if not exists_filename(filename):
            filename = ask_filename()

        set_image_label(image_label, filename)

        tk.Button(
            root,
            text="Change scheme",
            command=lambda: save_new_scheme(
                label=image_label, flashcard_id=flashcard_id
            ),
        ).pack()

        root.mainloop()
