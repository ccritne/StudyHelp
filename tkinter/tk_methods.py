# Imports
from datetime import date, datetime as dt, time, timedelta as td
import copy
import io
from io import BytesIO
import tkinter as tk
import matplotlib.pyplot as plt
from PIL import Image
import re
import ast
import textwrap
import base64
import os
from termcolor import colored

# Global variables:
from tk_setup import *


# =========================== #
# CHANGE PREVIOUS PAGE METHOD #
# =========================== #
def change_previous_page(old_page: str):
    # Importing the variable from the setup file:
    global previous_page
    previous_page = old_page


# ======================== #
# GET PREVIOUS PAGE METHOD #
# ======================== #
def get_previous_page() -> str:
    global previous_page
    return previous_page


# ========================= #
# CHANGE ACTUAL PAGE METHOD #
# ========================= #
def change_actual_page(new_page: str):
    global actual_page
    actual_page = new_page


# ====================== #
# GET ACTUAL PAGE METHOD #
# ====================== #
def get_actual_page() -> str:
    global actual_page
    return actual_page


# ============== #
# FROM TO METHOD #
# ============== #
def from_to(str_from: str, str_to: str, frame: tk.Frame):
    pass  # I don't know what this class should do -M
