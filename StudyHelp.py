from main_window import make_main_window
from functions import creation_db, update_all_deadlines

if __name__ == "__main__":
    creation_db()
    update_all_deadlines()
    make_main_window()
