import subprocess

def get_latest_commit_hash():
    try:
        # Get the short hash of the latest commit
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        return commit_hash.decode('utf-8').strip()
    except Exception as e:
        return f"unknown ({e})"

version = "" # Set the app version here

if not version:
    ver = get_latest_commit_hash()

else:
    ver = version
