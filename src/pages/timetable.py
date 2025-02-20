import flet as ft
from i18n import _


def TimetablePage():
    return ft.Column([
                ft.Text((_("Timetable")), size=30, weight="bold"),
                ft.Placeholder()
            ])
        
        