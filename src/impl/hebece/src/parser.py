import requests
import json
import uuid
import hashlib
import sqlite3
import os
import base64
from impl.hebece.src.signer import *
from impl.hebece.src.utils import *
from impl.hebece.src.api import *
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def getUserInfo(tenant):
    content, dinfo = HEBELogin(tenant)

    data = json.loads(content)
    envelope = data.get("Envelope", [])[0]

    pupil = envelope.get("Pupil", {})
    unit = envelope.get("Unit", {})
    links = envelope.get("Links", {})
    ConstituentUnit = envelope.get("ConstituentUnit", {})
    periods = envelope.get("Periods", [])


    Name = pupil.get("FirstName", {})
    SecondName = pupil.get("SecondName", {})
    Surname = pupil.get("Surname", {})
    Class = envelope.get("ClassDisplay", {})
    PupilID = pupil.get("Id", {})
    SchoolID = links.get("Symbol", {})
    ConstituentID = ConstituentUnit.get("Id", {})
    UnitID = unit.get("Id", {})
    PeriodID = next((period.get('Id') for period in periods if period.get('Current')), None)

    return Name, SecondName, Surname, Class, PupilID, SchoolID, ConstituentID, UnitID, PeriodID