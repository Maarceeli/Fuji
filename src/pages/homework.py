import flet as ft
from i18n import _


def HomeworkPage():
    return ft.Column([
                ft.Text((_("Homework")), size=30, weight="bold"),
                ft.Placeholder()
            ])
        
        