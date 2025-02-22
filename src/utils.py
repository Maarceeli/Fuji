import keyring

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
