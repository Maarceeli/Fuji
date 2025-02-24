from utils import getconfigpath
import configparser
import gettext
import locale
import json
import os

# Determine the user's locale
try:
    config = configparser.ConfigParser()
    config.read(f"{getconfigpath()}/config.ini")
    lang = config["Settings"]["language"]
except FileNotFoundError:
    lang = "pl"
    print("Defaulting to Polish due to missing config file")
except AttributeError:
    lang = "pl"
    print("Defaulting to Polish due to missing language setting in config file")
except Exception as e:
    lang = "pl"
    print(f"Defaulting to Polish due to error: {e}")
finally:
    print(f"Language set to {lang}")

# Set up translation
localedir = os.path.join(os.path.dirname(__file__), "locales")
translation = gettext.translation("base", localedir, languages=[lang], fallback=False)
translation.install()
_ = translation.gettext  # Shortcut for gettext

# Function to switch language dynamically
def set_language(new_lang):
    global translation, _
    translation = gettext.translation("base", localedir, languages=[new_lang], fallback=False)
    translation.install()
    _ = translation.gettext  # Update global _
