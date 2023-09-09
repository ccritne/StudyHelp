import sqlite3
import datetime

con = sqlite3.connect("datas.db")
cursor = con.cursor()

previousPage = None
actualPage = None

rowSources = None
rowFlashcards = None

sourcesNames = []
flashcards = []
sourcesArray = []
flashcardsArray = []
tableDeck = []

playedSourceID = None
playedFlashcardID = None

selectedSourceID = None
selectedFlashcardID = None

frontInputSelected = False
backInputSelected = False

weekdays = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
weekdays_complete = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

selectedDate = None
