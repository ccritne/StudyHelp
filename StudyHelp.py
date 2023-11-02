from main_window import make_main_window
from functions import creationDB, updateAllDeadlines

if __name__ == "__main__":
    creationDB()
    updateAllDeadlines()
    make_main_window()
