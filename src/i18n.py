from utils import getconfigpath
import configparser
import gettext
import json
import os
import sys

# Detect if running as a compiled Nuitka binary
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS  # Nuitka extracts files here
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Running locally

# Determine the user's locale
try:
    config = configparser.ConfigParser()
    config.read(os.path.join(getconfigpath(), "config.ini"))
    lang = config.get("Settings", "language", fallback="pl")
except FileNotFoundError:
    lang = "pl"
    print("Defaulting to Polish due to missing config file")
except Exception as e:
    lang = "pl"
    print(f"Defaulting to Polish due to error: {e}")
finally:
    print(f"Language set to {lang}")

# Determine the correct locales directory
if getattr(sys, 'frozen', False):
    # Running as a compiled binary
    localedir = os.path.join(BASE_DIR, "src", "locales")
else:
    # Running locally
    localedir = os.path.join(BASE_DIR, "locales")

# Ensure .mo files exist
def ensure_mo_files():
    for root, _, files in os.walk(localedir):
        for file in files:
            if file.endswith(".po"):
                mo_file = file.replace(".po", ".mo")
                mo_path = os.path.join(root, mo_file)
                if not os.path.exists(mo_path):
                    po_path = os.path.join(root, file)
                    print(f"Compiling {po_path} to {mo_path}")
                    os.system(f"msgfmt {po_path} -o {mo_path}")

if not getattr(sys, 'frozen', False):  # Only check when running locally
    ensure_mo_files()

# Function to load translations safely
def load_translation(language):
    try:
        return gettext.translation("base", localedir, languages=[language], fallback=True)
    except FileNotFoundError:
        print(f"Warning: Translation file not found for language '{language}'")
        return gettext.NullTranslations()

# Load initial language
translation = load_translation(lang)
translation.install()
_ = translation.gettext  # Shortcut for gettext

# Function to switch language dynamically
def set_language(new_lang):
    global translation, _
    translation = load_translation(new_lang)
    translation.install()
    _ = translation.gettext  # Update global _
