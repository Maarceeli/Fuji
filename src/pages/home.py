import flet as ft
import configparser
from i18n import _
from constants import *
from components.home import RecentGradesCard, UserProfileCard, TimetableCard, UserStatsCard
from utils import getconfigpath, format_lessons, restart
from sqlitehandlernr import fetch_timetable_for_day
from datetime import datetime

def HomePage(lucky_number, page):
    config = configparser.ConfigParser()
    config.read(f"{getconfigpath()}/config.ini")

    studentFullName = config['User']['fullName']
    studentClass = config['User']['grade']
    
    timetable = fetch_timetable_for_day(datetime.today())
    
    if timetable == 0:
        restart(page)

    lessons = format_lessons(timetable)

    return ft.Column([
        ft.Text((_("Home")), size=30, weight="bold"),
        ft.Text("\n", size=30, weight="bold"),
        ft.Row([
            UserProfileCard(studentFullName, studentClass),
            UserStatsCard(lucky_number),
        ]),
        ft.Row([
            TimetableCard(lessons),
            RecentGradesCard()
        ]),
    ])