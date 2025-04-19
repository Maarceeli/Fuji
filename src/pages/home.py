import flet as ft
import configparser
from i18n import _
from constants import *
from components.home import RecentGradesCard, UserProfileCard, TimetableCard, UserStatsCard
from utils import getconfigpath

def HomePage(lucky_number):
    config = configparser.ConfigParser()
    config.read(f"{getconfigpath()}/config.ini")

    studentFullName = config['User']['fullName']
    studentClass = config['User']['grade']
    
    return ft.Column([
        ft.Text((_("Home")), size=30, weight="bold"),
        ft.Text("\n", size=30, weight="bold"),
        ft.Row([
            UserProfileCard(studentFullName, studentClass),
            UserStatsCard(lucky_number),
        ]),
        ft.Row([
            TimetableCard(),
            RecentGradesCard()
        ]),
    ])