# Fuji

Unofficial eduVulcan client for PC

Full of programming warcrimes

## Installation

```sh
pip install -r requirements.txt
```

## Compilation

```sh
pip install nuitka
nuitka --onefile --include-data-dir=src/locales=src/locales src/main.py
```