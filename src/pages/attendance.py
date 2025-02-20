import flet as ft
from i18n import _

def AttendancePage():
    return ft.Column([
                ft.Text((_("Attendance")), size=30, weight="bold"),
                ft.Placeholder()
            ])
        
        