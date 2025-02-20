import flet as ft
from i18n import _


def GradesPage():
    return ft.Column([
                ft.Text((_("Grades")), size=30, weight="bold"),
                ft.Placeholder()
            ])
        
        