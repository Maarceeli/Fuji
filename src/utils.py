import os
from pathlib import Path
from datetime import datetime, timedelta
import configparser
import subprocess
import sys
import flet as ft
    
def getconfigpath():
    platform = os.name
    home = Path.home()
    
    match platform:
        case 'posix':
            return f"{home}/.config/Fuji"
        case 'Darwin':
            return f"{home}/.FujiConfig"
        case 'nt':
            return f"{home}/AppData/Local/Fuji"

def getthemecolor():
    config = configparser.ConfigParser()
    config.read(f"{getconfigpath()}/config.ini")
    color = config['Settings']['themecolor']
    
    return color

def setthemecolor(color):
    config = configparser.ConfigParser()
    config.read(f"{getconfigpath()}/config.ini")
    config["Settings"]["themecolor"] = color
    
    with open(f"{getconfigpath()}/config.ini", "w") as file:
        config.write(file)
        
def setlanguage(lang):
    config = configparser.ConfigParser()
    config.read(f"{getconfigpath()}/config.ini")
    
    match lang.data:
        case "Polski":
            config["Settings"]["language"] = "pl"
        case "English":
            config["Settings"]["language"] = "en"
    
    with open(f"{getconfigpath()}/config.ini", "w") as file:
        config.write(file)
        
def getcurrentsemester():
    config = configparser.ConfigParser()
    config.read(f"{getconfigpath()}/config.ini")
    
    try:
        semester = int(config['User']['semester'])
    except ValueError:
        semester = 1
    
    return semester

def setcurrentsemester(semester):
    config = configparser.ConfigParser()
    config.read(f"{getconfigpath()}/config.ini")
    
    try:
        config["User"]["semester"] = str(semester.number)
    except ValueError:
        config["User"]["semester"] = "1"
    
    with open(f"{getconfigpath()}/config.ini", "w") as file:
        config.write(file)

def restart(page: ft.Page):
    try:
        python = sys.executable
        subprocess.Popen([python] + sys.argv)
        page.window.destroy()
    except FileNotFoundError:
        exit()
        
def get_current_month_dates():
    today = datetime.today()
    start_date = today.replace(day=1)
    # To get the last day, move to the next month, then subtract one day
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    end_date = next_month - timedelta(days=1)
    
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

def getinitials(full_name):
    initials = ''.join([part[0].upper() for part in full_name.split()])
    return initials

def logout():
    config = configparser.ConfigParser()
    config.read(f"{getconfigpath()}/config.ini")
    config["Settings"]["islogged"] = "False"
    config["User"]["fullname"] = ""
    config["User"]["grade"] = ""
    config["User"]["semester"] = "1"

    if os.path.exists("database.db"):
        os.remove("database.db")
    
    with open(f"{getconfigpath()}/config.ini", "w") as file:
        config.write(file)
        
def format_grade(grade):
    """
    Format a single grade into a readable string.
    """
    # Access the grade value as an attribute, not as a dictionary key
    return str(grade.value)

def calculate_weighted_average(grades_list):
    valid_grades = [g for g in grades_list if parse_grade_value(g.value) is not None and g.weight > 0]
    total_weight = sum(g.weight for g in valid_grades)
    if total_weight == 0:
        return 0.0
    weighted_sum = sum(parse_grade_value(g.value) * g.weight for g in valid_grades)
    return weighted_sum / total_weight

def parse_grade_value(value):
    try:
        base_value = float(value.rstrip('+-'))
        if value.endswith('+'):
            return base_value + 0.25
        elif value.endswith('-'):
            return base_value - 0.25
        return base_value
    except ValueError:
        return None
    
def format_date(dt):
    return dt.strftime("%Y/%m/%d")