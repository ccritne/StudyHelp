import datetime
from datetime import datetime
import sqlite3

con = sqlite3.connect("datas.db")
cursor = con.cursor()

previous_page: str | None = None
actual_page: str | None = None

row_sources: int | None = None
row_flashcards: int | None = None

sources_names: list = []
flashcards: list = []
sources_array: list = []
flashcards_array: list = []
table_deck: list = []

played_source_ID: int | None = None
played_flashcard_ID: int | None = None

selected_source_ID: int | None = None
selected_flashcard_ID: int | None = None

front_input_selected: bool = False
back_input_selected: bool = False

WEEKDAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
FULL_WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

selected_date: datetime | str | None = None

front_layout: list[list] = [[]]
back_layout: list[list] = [[]]
