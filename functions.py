from setup import *
from datetime import date, datetime, time, timedelta
import copy
from io import BytesIO as StringIO
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from PIL import Image
import re
import ast

def changePreviousPage(oldPage):
    global previousPage
    previousPage = oldPage

def getPreviousPage():
    global previousPage
    return previousPage

def changeActualPage(newPage):
    global actualPage
    actualPage = newPage

def getActualPage():
    global actualPage
    return actualPage

def FromTo(str_from, str_to, window):
    window[str_from].update(visible=False)
    window[str_to].update(visible=True)
    changePreviousPage(str_from)
    changeActualPage(str_to)

def calculateDeadline(
        arrSessionWeek, 
        totalPages, 
        studiedPages
        ):

    todayDate = datetime.now()
    todayIndex = todayDate.weekday()

    deadline = copy(todayDate)
    remainingPages = totalPages - studiedPages

    daysToAdd = 0

    while todayIndex < 7:

        if arrSessionWeek[weekdays[todayIndex]]['isStudyDay']:
            remainingPages -= min(arrSessionWeek[weekdays[todayIndex]]['totalPages'], remainingPages)
        
        todayIndex += 1
        if remainingPages > 0:
            daysToAdd += 1

    deadline += timedelta(days=daysToAdd)

    weekPages = arrSessionWeek['totalPages']
    weeksAdd = (int(remainingPages/weekPages) - 1)
    daysAdd = weeksAdd*7
    remainingPages -= (weekPages* weeksAdd)
    deadline += timedelta(days = daysAdd)

    todayIndex = 0

    daysToAdd = 0
    while remainingPages > 0:

        if arrSessionWeek[weekdays[todayIndex]]['isStudyDay']:
            remainingPages -= min(arrSessionWeek[weekdays[todayIndex]]['totalPages'], remainingPages)
        
        if todayIndex < 6:
            todayIndex += 1
        else:
            todayIndex = 0

        if remainingPages > 0:
            daysToAdd += 1

    deadline += timedelta(days=daysToAdd)

    return deadline.strftime('%d-%m-%Y')    

def allSourcesNames():
    cursor.execute('SELECT DISTINCT id, name FROM sources')
    return cursor.fetchall()

def getFlashcards(sourceID):
    cursor.execute(f'SELECT ID, front, back, deadline, box FROM flashcards WHERE sourceID = {sourceID}')
    return cursor.fetchall()

def getTodayFlashcardsSource(sourceIDs):
    todayStr = datetime.now().strftime('%Y-%m-%d')
    query = f"""SELECT ID, front, back, box, sourceID FROM flashcards WHERE deadline='{todayStr}' AND sourceID in {tuple(sourceIDs) if len(sourceIDs) > 1 else "("+str(sourceIDs[0])+")"}"""
    cursor.execute(query)
    return cursor.fetchall()

def getInfoDecks():
    
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

def getSettingsValue(value):

        cursor.execute('SELECT '+value+' FROM settings')
        
        return cursor.fetchone()[0]

def render_latex(formula, fontsize=12, dpi=300, format_='png'):
    """Renders LaTeX formula into image.
    """
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, u'${}$'.format(formula), fontsize=fontsize)
    buffer_ = StringIO()
    fig.savefig(buffer_, dpi=dpi, transparent=False, format=format_, bbox_inches='tight', pad_inches=0.0)
    plt.close(fig)
    return buffer_.getvalue()

def setSelectedSourceID(id):
    global selectedSourceID
    selectedSourceID = id

def getSelectedBookID():
    global selectedSourceID
    return selectedSourceID

def setSelectedFlashcardID(id):
    global selectedFlashcardID
    selectedFlashcardID = id

def getSelectedFlashcardID():

    global selectedFlashcardID
    return selectedFlashcardID

def setPlayedSourceID(id):
    global playedSourceID
    playedSourceID = id

def getPlayedSourceID():
    global playedSourceID
    return playedSourceID

def setPlayedFlashcardID(id):
    global playedFlashcardID
    playedFlashcardID = copy.deepcopy(id)

def convert_to_bytes(file_or_bytes, resize=None):
    if file_or_bytes is not None:
        img = Image.open(file_or_bytes)
        if resize is not None:
            img = img.resize(resize)
        with io.BytesIO() as bio:
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
    else:
        return None
    
def getPlayedFlashcardID():
    global playedFlashcardID
    return playedFlashcardID

def getSourceValues(bookID):
    cursor.execute(f'SELECT * FROM sources WHERE ID={bookID}')
    
    return cursor.fetchone()

def getFlashcardsArray():
    global flashcardsArray
    return flashcardsArray

def setFlashcardsArray(fArray):
    global flashcardsArray
    flashcardsArray = fArray[:]

def checkStrIntInput(str):
    regexp = re.compile('[^0-9]')
    if regexp.search(str) or len(str) == 0:
        return False
    
    return True

def setSourcesArray(bArray):
    global sourcesArray
    sourcesArray = copy.copy(bArray)

def getSourcesArray():
    global sourcesArray
    return sourcesArray

def setTableDeck(tDeck):
    global tableDeck
    tableDeck = copy.copy(tDeck)

def getTableDeck():
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

    return totalMinutes

def setRowSources(row):
    global rowSources
    rowSources = row

def getRowSources():
    global rowSources
    return rowSources

def setRowFlashcards(row):
    global rowFlashcards
    rowFlashcards = copy.copy(row)

def getRowFlashcards():
    global rowFlashcards
    return rowFlashcards

def setFrontInputSelected(value):
    global frontInputSelected
    frontInputSelected = copy.copy(value)

def getFrontInputSelected():
    global frontInputSelected
    return frontInputSelected

def setBackInputSelected(value):
    global backInputSelected
    backInputSelected = copy.copy(value)

def getBackInputSelected():
    global backInputSelected
    return backInputSelected

def setSelectedDate(date):
    global selectedDate
    selectedDate = copy.copy(date)

def getSelectedDate() -> datetime:
    global selectedDate
    return selectedDate

def getStringDate(date):
    return date.strftime('%Y-%m-%d')

def getStringDateWithTime(date):
    return date.strftime('%Y-%m-%d %H:%M')