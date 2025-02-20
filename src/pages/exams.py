import flet as ft
from i18n import _


def ExamsPage():
    return ft.Column([
                ft.Text((_("Exams")), size=30, weight="bold"),
                ft.Placeholder()
            ])
        
        