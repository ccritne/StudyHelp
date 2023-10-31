from mainWindow import makeMainWindow
from functions import creationDB, updateAllDeadlines

if __name__ == "__main__":
    creationDB()
    updateAllDeadlines()
    makeMainWindow()