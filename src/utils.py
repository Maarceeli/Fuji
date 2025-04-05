import keyring
import os
from pathlib import Path
import configparser
import subprocess
import sys
import flet as ft

def saveauth(service, username, data, chunk_size=1000):
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    keyring.set_password(service, f"{username}_count", str(len(chunks)))
    
    for i, chunk in enumerate(chunks):
        keyring.set_password(service, f"{username}_{i}", chunk)
    
def loadauth(service, username):
    try:
        count = int(keyring.get_password(service, f"{username}_count"))
        return "".join(keyring.get_password(service, f"{username}_{i}") or "" for i in range(count))
    except (TypeError, ValueError):
        return None
    
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