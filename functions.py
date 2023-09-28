from setup import *
from datetime import date, datetime, time, timedelta
import copy
from io import BytesIO
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from PIL import Image
import re
import ast
import textwrap
import base64
import os

def changePreviousPage(oldPage : str):
    global previousPage
    previousPage = oldPage

def getPreviousPage() -> str:
    global previousPage
    return previousPage

def changeActualPage(newPage : str):
    global actualPage
    actualPage = newPage

def getActualPage() -> str:
    global actualPage
    return actualPage

def FromTo(str_from : str, str_to : str, window : sg.Window):
    window[str_from].update(visible=False)
    window[str_to].update(visible=True)
    changePreviousPage(str_from)
    changeActualPage(str_to)

def calculateDeadline(
        arrSessionWeek : list,
        isBook : bool = True,
        # isVideo: bool = False,
        totalPages : int | None = 0, 
        studiedPages : int | None = 0,
        # totalMinutes : int | None = 0, 
        # viewedMinutes : int | None = 0,  
        ) -> datetime:

    todayDate = datetime.now()
    todayIndex = todayDate.weekday()

    deadline : datetime = copy.copy(todayDate) 
    remaining = 0
    
    indexStr = ''

    # if isVideo:
    #    remaining = totalMinutes - viewedMinutes
    #    indexStr = 'totalDuration'

    if isBook:
        remaining = totalPages - studiedPages
        indexStr = 'totalPages'

    daysToAdd = 0

    while todayIndex < 7:
        if arrSessionWeek[weekdays[todayIndex]]['isStudyDay'] and arrSessionWeek[weekdays[todayIndex]]['areThereSessions']:
            remaining -= min(arrSessionWeek[weekdays[todayIndex]][indexStr], remaining)
        
        todayIndex += 1
        if remaining > 0:
            daysToAdd += 1

    deadline += timedelta(days=daysToAdd)
    
    weekDo = arrSessionWeek[indexStr]

    weeksAdd = int(remaining/weekDo)

    if weeksAdd > 0:
        weeksAdd -= 1

    daysAdd = weeksAdd*7
    remaining -= (weekDo * weeksAdd)
    deadline += timedelta(days = daysAdd)

    
    todayIndex = 0

    daysToAdd = 0
    while remaining > 0:

        if arrSessionWeek[weekdays[todayIndex]]['isStudyDay'] and arrSessionWeek[weekdays[todayIndex]]['areThereSessions']:
            remaining -= min(arrSessionWeek[weekdays[todayIndex]][indexStr], remaining)
        
        if todayIndex < 6:
            todayIndex += 1
        else:
            todayIndex = 0

        if remaining > 0:
            daysToAdd += 1

    deadline += timedelta(days=daysToAdd)

    return deadline   

def allSourcesNames() -> list:
    cursor.execute('SELECT DISTINCT id, name FROM sources')
    result = cursor.fetchall()
    
    return result

def getFlashcardsForTable(sourceID : int) -> list:
    cursor.execute(f'SELECT ID, front, back, deadline, box FROM flashcards WHERE sourceID = {sourceID}')
    result = cursor.fetchall()
    
    return result

def getTodayFlashcardsSource(sourceID : int) -> list:
    todayStr = datetime.now().strftime('%Y-%m-%d')
    query = "SELECT ID, front, back, box, sourceID FROM flashcards WHERE deadline = ? AND sourceID = ? "
    parameters = (todayStr, sourceID)
    cursor.execute(query, parameters)

    result = cursor.fetchall()
    
    return result

def getInfoDecks() -> list:
    
    todayStr = datetime.now().strftime('%Y-%m-%d')
    cursor.execute(f'''SELECT sources.ID,
                                sources.name,
                                flashcards.deadline
                            FROM flashcards
                                LEFT JOIN
                                sources ON flashcards.sourceID = sources.ID
                            ORDER BY sources.ID;
                        ''')
    
    array = cursor.fetchall()
    if array != []:
        id = array[0][0]
        tableInfo = [[id, array[0][1], 0]]
        index = 0
        for x in range(len(array)):
            if array[x][0] != id: # Sort fetch
                id = array[x][0]
                tableInfo.append([id, array[x][1], 0])
                index += 1
            
            if array[x][2] == todayStr:
                tableInfo[index][2] += 1

                
        return tableInfo

    return [[]]

def getSettingsValue(value : str) -> str | int:

    cursor.execute('SELECT '+value+' FROM settings')
    
    return cursor.fetchone()[0]

def render_latex(formula : str, fontsize : int = 12, dpi : int = 300, format_ : str='png') -> bytes:
    """Renders LaTeX formula into image.
    """
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, u'${}$'.format(formula), fontsize=fontsize)
    buffer_ = BytesIO()
    fig.savefig(buffer_, dpi=dpi, transparent=False, format=format_, bbox_inches='tight', pad_inches=0.0)
    plt.close(fig)
    return buffer_.getvalue()

def setSelectedSourceID(id : int | None):
    global selectedSourceID
    selectedSourceID = id

def getSelectedSourceID() -> int | None:
    global selectedSourceID
    return selectedSourceID

def setSelectedFlashcardID(id : int | None):
    global selectedFlashcardID
    selectedFlashcardID = id

def getSelectedFlashcardID() -> int | None:

    global selectedFlashcardID
    return selectedFlashcardID

def setPlayedSourceID(id : int | None):
    global playedSourceID
    playedSourceID = id

def getPlayedSourceID() -> int | None:
    global playedSourceID
    return playedSourceID

def setPlayedFlashcardID(id : int | None):
    global playedFlashcardID
    playedFlashcardID = id

def convert_to_bytes(filename, resize=None) -> bytes:
    try:
        img = Image.open(filename)
        if resize is not None:
            img = img.resize(resize)
        with BytesIO() as bio:
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
    except:        
        return None
    
def getPlayedFlashcardID() -> int | None:
    global playedFlashcardID
    return playedFlashcardID

def getSourceValues(sourceID : int) -> tuple:
    cursor.execute(f'SELECT * FROM sources WHERE ID={sourceID}')
    
    return cursor.fetchone()

def getFlashcardsArray() -> list:
    global flashcardsArray
    return flashcardsArray

def appendFlashcard(flashcard : tuple):
    global flashcardsArray
    flashcardsArray.append(flashcard)

def removeFlashcard(index : int):
    global flashcardsArray
    flashcardsArray.pop(index)

def setFlashcardsArray(fArray : list):
    global flashcardsArray
    flashcardsArray = copy.copy(fArray)

def checkStrIntInput(str) -> bool:
    regexp = re.compile('[^0-9]')
    if regexp.search(str) or len(str) == 0:
        return False
    
    return True

def setSourcesArray(bArray : list):
    global sourcesArray
    sourcesArray = copy.copy(bArray)

def getSourcesArray() -> list:
    global sourcesArray
    return sourcesArray

def setTableDeck(tDeck : list):
    global tableDeck
    tableDeck = copy.copy(tDeck)

def getTableDeck() -> list:
    global tableDeck
    return tableDeck 

def getTotalMinutes(indexDay, exceptID=None):
    query = 'SELECT arrSessions FROM sources '

    if exceptID is not None:
        query = query + ' WHERE ID <> ' + str(exceptID)
    
    cursor.execute(query)
    result = cursor.fetchall()
    totalMinutes = 0
    for x in result:
        json = ast.literal_eval(x[0])
        if json[weekdays[indexDay]]['isStudyDay'] and json[weekdays[indexDay]]['areThereSessions']:
            totalMinutes += json[weekdays[indexDay]]['totalDuration']
        if json['withLectures'] and json[weekdays[indexDay]]['areThereLectures']:
            totalMinutes += json[weekdays[indexDay]]['timeLectures']['durationLecture']

    return totalMinutes

def setRowSources(row : int):
    global rowSources
    rowSources = row

def getRowSources() -> int:
    global rowSources
    return rowSources

def setRowFlashcards(row : int):
    global rowFlashcards
    rowFlashcards = row

def getRowFlashcards() -> int:
    global rowFlashcards
    return rowFlashcards

def setFrontInputSelected(value : bool):
    global frontInputSelected
    frontInputSelected = value

def getFrontInputSelected() -> bool:
    global frontInputSelected
    return frontInputSelected

def setBackInputSelected(value : bool):
    global backInputSelected
    backInputSelected = value

def getBackInputSelected() -> bool | None:
    global backInputSelected
    return backInputSelected

def setSelectedDate(date : datetime):
    global selectedDate
    selectedDate = copy.copy(date)

def getSelectedDate() -> datetime | None:
    global selectedDate
    return selectedDate

def getStringDate(date : datetime) ->  str:
    return date.strftime('%Y-%m-%d')

def getStringDateWithTime(date : datetime) -> str:
    return date.strftime('%Y-%m-%d %H:%M')

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

def fromTextToElements(text : str):
    elements = []

    startLatex = False
    stringLatex = ""
    normalString = ""

    x = 0
    while x < len(text):

        if x + 6 < len(text) and text[x:x+7] == '[latex]':
            if len(normalString)> 0 :
                elements.append([sg.Text(text=textwrap.fill(normalString), expand_x=True)])
            normalString = ""
            startLatex = True
            x += 7

        if x + 7 < len(text) and text[x:x+8] == '[/latex]':

            if len(stringLatex)> 0 : 
                image_bytes = render_latex(stringLatex)
                image_base64 = base64.b64encode(image_bytes)
                elements.append([sg.Column([[sg.Image(source=image_base64)]])])
            startLatex = False
            stringLatex = ""
            x += 8

        if x < len(text):
            if startLatex:
                stringLatex += text[x]
            else:
                normalString += text[x]
            x += 1

    if len(normalString)> 0:
        elements.append([sg.Text(textwrap.fill(normalString), expand_x=True)])
    
    return elements

def fromNumberToTime(number : int) -> str:
    if number < 10:
        return "0"+str(number)
    
    return str(number)
    

def existsFilename(filename):

    if filename in [None, "", 'EXIT_WINDOW', 'FILE_NOT_FOUND']:
        return False
    
    isFile = os.path.isfile(filename)

    return isFile

def existsImg(img):

    if img in [None]:
        return False

    return True