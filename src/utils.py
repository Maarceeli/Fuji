import keyring
import os
from pathlib import Path

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
