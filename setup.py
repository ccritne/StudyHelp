import datetime
from datetime import datetime
import sqlite3

con = sqlite3.connect("datas.db")
cursor = con.cursor()

previousPage : str | None = None
actualPage : str | None = None

rowSources :int | None = None
rowFlashcards : int | None = None

sourcesNames : list = []
flashcards : list = []
sourcesArray : list = []
flashcardsArray : list = []
tableDeck : list = []

playedSourceID : int | None = None
playedFlashcardID : int | None = None

selectedSourceID : int | None = None
selectedFlashcardID : int | None = None

frontInputSelected : bool = False
backInputSelected : bool = False

WEEKDAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
FULL_WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

selectedDate : datetime | str | None = None

frontLayout : list[list] = [[]]
backLayout : list[list] = [[]]