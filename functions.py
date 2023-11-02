import sqlite3
from setup import con, cursor, WEEKDAYS
from tkinter import *
import PySimpleGUI as sg
from datetime import datetime, timedelta
import copy
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import re
import ast
import textwrap
import base64
import os


def changePreviousPage(oldPage: str):
    global previousPage
    previousPage = oldPage


def getPreviousPage() -> str:
    global previousPage
    return previousPage


def changeActualPage(newPage: str):
    global actualPage
    actualPage = newPage


def getActualPage() -> str:
    global actualPage
    return actualPage


def FromTo(str_from: str, str_to: str, window: sg.Window):
    window[str_from].update(visible=False)
    window[str_to].update(visible=True)
    changePreviousPage(str_from)
    changeActualPage(str_to)


def calculateDeadline(
    arrSessionWeek: list,
    isBook: bool = True,
    totalPages: int | None = 0,
    studiedPages: int | None = 0,
) -> datetime:
    todayDate = datetime.now()
    todayIndex = todayDate.weekday()

    deadline: datetime = copy.copy(todayDate)
    remaining = 0

    indexStr = ""

    if isBook:
        remaining = totalPages - studiedPages
        indexStr = "totalPages"

    daysToAdd = 0

    while todayIndex < 7:
        if (
            arrSessionWeek[WEEKDAYS[todayIndex]]["isStudyDay"]
            and arrSessionWeek[WEEKDAYS[todayIndex]]["areThereSessions"]
        ):
            remaining -= min(arrSessionWeek[WEEKDAYS[todayIndex]][indexStr], remaining)

        todayIndex += 1
        if remaining > 0:
            daysToAdd += 1

    deadline += timedelta(days=daysToAdd)

    weekDo = arrSessionWeek[indexStr]

    weeksAdd = int(remaining / weekDo)

    if weeksAdd > 0:
        weeksAdd -= 1

    daysAdd = weeksAdd * 7
    remaining -= weekDo * weeksAdd
    deadline += timedelta(days=daysAdd)

    todayIndex = 0

    daysToAdd = 0
    while remaining > 0:
        if (
            arrSessionWeek[WEEKDAYS[todayIndex]]["isStudyDay"]
            and arrSessionWeek[WEEKDAYS[todayIndex]]["areThereSessions"]
        ):
            remaining -= min(arrSessionWeek[WEEKDAYS[todayIndex]][indexStr], remaining)

        if todayIndex < 6:
            todayIndex += 1
        else:
            todayIndex = 0

        if remaining > 0:
            daysToAdd += 1

    deadline += timedelta(days=daysToAdd)

    return deadline


def allSourcesNames() -> list:
    cursor.execute("SELECT id, name FROM sources")
    result = cursor.fetchall()

    return result


def getFlashcardsForTable(sourceID: int) -> list:
    cursor.execute(
        "SELECT ID, front, back, deadline, box FROM flashcards WHERE sourceID = ?",
        (sourceID,),
    )
    result = cursor.fetchall()

    return result


def getTodayFlashcardsSource(sourceID: int) -> list:
    todayStr = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "SELECT ID, front, back, box, sourceID FROM flashcards WHERE deadline = ? AND sourceID = ? ",
        (todayStr, sourceID),
    )

    result = cursor.fetchall()

    return result


def getInfoDecks() -> list:
    todayStr = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        """ SELECT sources.ID,
                sources.name,
                flashcards.deadline
            FROM flashcards
                LEFT JOIN
                sources ON flashcards.sourceID = sources.ID
            ORDER BY sources.ID;
        """
    )

    array = cursor.fetchall()
    if array != []:
        id = array[0][0]
        tableInfo = [[id, array[0][1], 0]]
        index = 0
        for x in range(len(array)):
            if array[x][0] != id:  # Sort fetch
                id = array[x][0]
                tableInfo.append([id, array[x][1], 0])
                index += 1

            if array[x][2] == todayStr:
                tableInfo[index][2] += 1

        return tableInfo

    return [[]]


def getSettingsValue(value: str) -> str | int:
    cursor.execute("SELECT " + value + " FROM settings")

    return cursor.fetchone()[0]


def render_latex(
    formula: str, fontsize: int = 12, dpi: int = 300, format_: str = "png"
) -> bytes:
    # Create a figure with the specified size and add the LaTeX formula
    fig, ax = plt.subplots(figsize=(0.01, 0.01))
    ax.text(0, 0, "${}$".format(formula), fontsize=fontsize)

    # Save the figure to a BytesIO buffer
    buffer = BytesIO()
    fig.savefig(
        buffer,
        dpi=dpi,
        transparent=False,
        format=format_,
        bbox_inches="tight",
        pad_inches=0.0,
    )

    # Close the figure and return the image data
    plt.close(fig)
    return buffer.getvalue()


def setSelectedSourceID(id: int | None):
    global selectedSourceID
    selectedSourceID = id


def getSelectedSourceID() -> int | None:
    global selectedSourceID
    return selectedSourceID


def setSelectedFlashcardID(id: int | None):
    global selectedFlashcardID
    selectedFlashcardID = id


def getSelectedFlashcardID() -> int | None:
    global selectedFlashcardID
    return selectedFlashcardID


def convert_to_bytes(filename: str, resize: dict | None = None) -> bytes:
    try:
        img = Image.open(filename)
        if resize is not None:
            img = img.resize(resize)
        bIo = BytesIO()
        img.save(bIo, format="PNG")
        del img
        return bIo.getvalue()
    except:
        print("Error!")
        return None


def getSourceValues(sourceID: int) -> tuple:
    cursor.execute("SELECT * FROM sources WHERE ID=?", (sourceID,))

    return cursor.fetchone()


def getFlashcardsArray() -> list:
    global flashcardsArray
    return flashcardsArray


def appendFlashcard(flashcard: tuple):
    global flashcardsArray
    flashcardsArray.append(flashcard)


def removeFlashcard(index: int):
    global flashcardsArray
    flashcardsArray.pop(index)


def setFlashcardsArray(fArray: list):
    global flashcardsArray
    flashcardsArray = copy.copy(fArray)


def checkStrIntInput(str: str) -> bool:
    regexp = re.compile("[^0-9]")
    if regexp.search(str) or len(str) == 0:
        return False

    return True


def setSourcesArray(bArray: list):
    global sourcesArray
    sourcesArray = copy.copy(bArray)


def getSourcesArray() -> list:
    global sourcesArray
    return sourcesArray


def setTableDeck(tDeck: list):
    global tableDeck
    tableDeck = copy.copy(tDeck)


def getTableDeck() -> list:
    global tableDeck
    return tableDeck


def getTotalMinutes(indexDay: int, exceptID: int | None = None):
    query = "SELECT arrSessions FROM sources "

    if exceptID is not None:
        query = query + " WHERE ID <> " + str(exceptID)

    cursor.execute(query)
    result = cursor.fetchall()
    totalMinutes = 0
    for x in result:
        json = ast.literal_eval(x[0])
        if (
            json[WEEKDAYS[indexDay]]["isStudyDay"]
            and json[WEEKDAYS[indexDay]]["areThereSessions"]
        ):
            totalMinutes += json[WEEKDAYS[indexDay]]["totalDuration"]
        if json["withLectures"] and json[WEEKDAYS[indexDay]]["areThereLectures"]:
            totalMinutes += json[WEEKDAYS[indexDay]]["timeLectures"]["durationLecture"]

    return totalMinutes


def setRowSources(row: int):
    global rowSources
    rowSources = row


def getRowSources() -> int:
    global rowSources
    return rowSources


def setRowFlashcards(row: int):
    global rowFlashcards
    rowFlashcards = row


def getRowFlashcards() -> int:
    global rowFlashcards
    return rowFlashcards


def setFrontInputSelected(value: bool):
    global frontInputSelected
    frontInputSelected = value


def getFrontInputSelected() -> bool:
    global frontInputSelected
    return frontInputSelected


def setBackInputSelected(value: bool):
    global backInputSelected
    backInputSelected = value


def getBackInputSelected() -> bool | None:
    global backInputSelected
    return backInputSelected


def setSelectedDate(date: datetime):
    global selectedDate
    selectedDate = copy.copy(date)


def getSelectedDate() -> datetime | None:
    global selectedDate
    return selectedDate


def getStringDate(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def getStringDateWithTime(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M")


def setFrontLayout(frontLy: list):
    global frontLayout
    frontLayout = copy.deepcopy(frontLy)


def setBackLayout(backLy: list):
    global backLayout
    backLayout = copy.deepcopy(backLy)


def getFrontLayout() -> list:
    global frontLayout
    return frontLayout


def getBackLayout() -> list:
    global backLayout
    return backLayout


def fromTextToElements(text: str):
    elements = []
    normalString = ""

    x = 0
    while x < len(text):
        if text[x : x + 7] == "[latex]":
            if normalString:
                elements.append(
                    [sg.Text(text=textwrap.fill(normalString), expand_x=True)]
                )
            normalString = ""
            x += 7

        elif text[x : x + 8] == "[/latex]":
            if normalString:
                elements.append(
                    [sg.Text(text=textwrap.fill(normalString), expand_x=True)]
                )
            normalString = ""
            latex_content = text[x - 7 : x]
            image_bytes = render_latex(latex_content)
            image_base64 = base64.b64encode(image_bytes)
            elements.append([sg.Column([[sg.Image(data=image_base64)]])])
            x += 8

        else:
            normalString += text[x]
            x += 1

    if normalString:
        elements.append([sg.Text(text=textwrap.fill(normalString), expand_x=True)])

    return elements


def fromNumberToTime(number: int) -> str:
    if number < 10:
        return "0" + str(number)

    return str(number)


def existsFilename(filename):
    if filename in [None, "", "FILE_NOT_FOUND"]:
        return False

    isFile = os.path.isfile(filename)

    return isFile


def existsImg(img):
    if img in [None]:
        return False

    return True


def checkInputClick(event):
    if event == "frontInput_LClick":
        setBackInputSelected(False)
        setFrontInputSelected(True)

    if event == "backInput_LClick" or event == "frontInput_Tab":
        setFrontInputSelected(False)
        setBackInputSelected(True)


def addLatexToInputField(window):
    key = None
    if getFrontInputSelected():
        key = "front"

    if getBackInputSelected():
        key = "back"

    if key is not None:
        widget = window[key].Widget
        cursor_position = widget.index(INSERT)
        widget.insert(cursor_position, "[latex][/latex]")
        widget.mark_set(INSERT, f"{cursor_position}+7c")


def saveNewFlashcard(front, back, filename):
    textFront = front
    textBack = back
    box = 0
    deadline = datetime.now().strftime("%Y-%m-%d")
    sourceID = getSelectedSourceID()
    filenameScheme = filename

    cursor.execute(
        "INSERT INTO flashcards(front, back, box, deadline, sourceID, filenameScheme) VALUES (?, ?, ?, ?, ?, ?)",
        (textFront, textBack, box, deadline, sourceID, filenameScheme),
    )
    con.commit()


def updateFlashcard(flashcardID, front, back):
    cursor.execute(
        "UPDATE flashcards SET front = ?, back = ? WHERE ID = ?",
        (front, back, flashcardID),
    )
    con.commit()


def saveScheme(flashcardID, filename):
    exitMessage = "EXIT_SUCCESS"
    if existsFilename(filename):
        cursor.execute(
            "UPDATE flashcards SET filenameScheme=? WHERE ID=?", (filename, flashcardID)
        )
        con.commit()
    else:
        sg.popup_error("Path Wrong", keep_on_top=True, modal=True)
        exitMessage = "PATH_WRONG"

    return exitMessage


def creationDB():
    SQL_SOURCES = """ CREATE TABLE IF NOT EXISTS sources (
                                    ID           INTEGER     NOT NULL
                                                            UNIQUE,
                                    courseName   TEXT,
                                    name         TEXT        NOT NULL,
                                    numberPages  INTEGER (5),
                                    studiedPages INTEGER (5),
                                    filename     TEXT,
                                    deadline     TEXT (10),
                                    arrSessions  TEXT,
                                    insertDate   TEXT (10)   NOT NULL,
                                    PRIMARY KEY (
                                        ID AUTOINCREMENT
                                    )
                                ); """

    cursor.execute(SQL_SOURCES)
    con.commit()

    SQL_FLASHCARDS = """CREATE TABLE IF NOT EXISTS flashcards (
                                    ID             INTEGER     PRIMARY KEY AUTOINCREMENT
                                                            NOT NULL,
                                    front          TEXT        NOT NULL,
                                    back           TEXT,
                                    deadline       TEXT (10),
                                    box            INTEGER (2) NOT NULL,
                                    sourceID       INTEGER     NOT NULL,
                                    filenameScheme TEXT
                                );"""

    cursor.execute(SQL_FLASHCARDS)
    con.commit()

    SQL_SETTINGS = """CREATE TABLE IF NOT EXISTS settings (
                                    defaultHourNotification INTEGER (2) DEFAULT (15) 
                                                                        UNIQUE ON CONFLICT IGNORE,
                                    maxStudyHour            INTEGER (2) DEFAULT (8) 
                                                                        UNIQUE ON CONFLICT IGNORE,
                                    studyDays               TEXT (7)    DEFAULT [0000000]
                                                                        UNIQUE ON CONFLICT IGNORE,
                                    maxSubjectsDay          INTEGER (1) DEFAULT (1) 
                                                                        UNIQUE ON CONFLICT IGNORE
                                );"""

    cursor.execute(SQL_SETTINGS)
    con.commit()

    SQL_SETTINGS_DATA = """INSERT INTO settings(defaultHourNotification, maxStudyHour, studyDays, maxSubjectsDay) VALUES (15, 8, '0000000', 1);"""

    cursor.execute(SQL_SETTINGS_DATA)
    con.commit()

    SQL_CALENDAR = """CREATE TABLE IF NOT EXISTS calendar (
                                    ID            INTEGER   NOT NULL,
                                    type          TEXT,
                                    description   TEXT,
                                    insertedDay   TEXT (10) NOT NULL,
                                    date          TEXT (10) NOT NULL,
                                    timeStartDate TEXT (5),
                                    timeEndDate   TEXT (5),
                                    startSession  INTEGER,
                                    endSession    INTEGER,
                                    sourceID      INTEGER,
                                    PRIMARY KEY (
                                        ID AUTOINCREMENT
                                    )
                                );"""

    cursor.execute(SQL_CALENDAR)
    con.commit()


def updateAllDeadlines():
    cursor.execute("SELECT ID, numberPages, studiedPages, arrSessions FROM sources;")
    sources = cursor.fetchall()
    for x in sources:
        arrSessionWeek = ast.literal_eval(x[3])
        upDeadline = getStringDate(
            calculateDeadline(
                totalPages=x[1],
                studiedPages=x[2],
                arrSessionWeek=arrSessionWeek,
                isBook=True,
            )
        )
        cursor.execute(
            "UPDATE sources SET deadline = ? WHERE ID = ?;", (upDeadline, x[0])
        )
        con.commit()
