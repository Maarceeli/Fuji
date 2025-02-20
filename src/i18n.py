import gettext
import locale
import json
import os

# Determine the user's locale
try:
    with open("config.json", "r") as file:
        data = json.load(file)
    langf = data.get("lang")
    lang = langf
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
    print("Language set")
           
            
# Set up translation
localedir = os.path.join(os.path.dirname(__file__), "locales")
translation = gettext.translation("base", localedir, languages=[lang], fallback=True)
translation.install()
_ = translation.gettext  # Shortcut for gettext

# Function to switch language dynamically
def set_language(new_lang):
    global translation, _
    translation = gettext.translation("base", localedir, languages=[new_lang], fallback=True)
    translation.install()
    _ = translation.gettext  # Update global _
