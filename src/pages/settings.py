import flet as ft
from i18n import _


def SettingsPage():
    return ft.Column([
                ft.Text((_("Settings")), size=30, weight="bold"),
                ft.Placeholder()
            ])
        
        