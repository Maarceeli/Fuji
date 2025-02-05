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

if __name__ == '__main__':
    debug = True
else:    
    debug = False

def getDebugInfo(data):
    data = json.loads(data)
    status = data.get("Status", {})
    code = status.get("Code")
    message = status.get("Message")
    return code, message

def getUserInfo(tenant):
    content = HEBELogin(tenant)

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

if __name__ == '__main__':
    today = datetime.today().strftime('%d-%m-%y')
    start_date, end_date = get_current_week()
    
    token = APILogin(login, password)
    tenant = get_tenant_from_jwt(token)
    content, dinfoJWT = JWTLogin(token, debug=debug)
    content, dinfoHEBE = HEBELogin(tenant, debug=debug)

    Name, SecondName, Surname, Class, PupilID, SchoolID, ConstituentID, UnitID, PeriodID = getUserInfo(tenant)
    print(Name, Surname, Class, PupilID, SchoolID, ConstituentID)

    LuckyNumber, LuckyNumberDay, dinfoLUCK = getLuckyNumber(tenant=tenant, schoolid=SchoolID, pupilid=PupilID, constituentid=ConstituentID, debug=debug)
    print(f"Lucky number: {LuckyNumber}")

    content, dinfoGRADE = getGrades(tenant=tenant, schoolid=SchoolID, pupilid=PupilID, unitid=UnitID, periodid=PeriodID, debug=debug)

    response, dinfoTIME = getTimetable(tenant=tenant, schoolid=SchoolID, pupilid=PupilID, start_date=start_date, end_date=end_date, debug=debug)
    

    r = getTimetableForDay(day=today)
    print(f"\nLessons for {today}:")
    
    if r == []:
        print("No lessons for today")
    else:
        for lesson in r:
            print(*lesson)

    content, dinfoEXAM = getExams(tenant=tenant, schoolid=SchoolID, pupilid=PupilID, start_date=start_date, end_date=end_date, debug=debug)

    ImportExamsToSQLite(content)
    print("Exams imported to SQLite database")

    exams = getExamsForWeek(start_date, end_date)
    for exam in exams:
        print(*exam)
    
    print(f"\nJWT Status: {dinfoJWT[0]} {dinfoJWT[1]}")
    print(f"HEBE Status: {dinfoHEBE[0]} {dinfoHEBE[1]}")
    print(f"Lucky Number Status: {dinfoLUCK[0]} {dinfoLUCK[1]}")
    print(f"Grades Status: {dinfoGRADE[0]} {dinfoGRADE[1]}")
    print(f"Timetable Status: {dinfoTIME[0]} {dinfoTIME[1]}")
    print(f"Exams Status: {dinfoEXAM[0]} {dinfoEXAM[1]}")