import flet as ft
from constants import *
from utils import setthemecolor, setlanguage
from i18n import _

def SettingsPage():
    def getlangoptions():
        return [
            ft.DropdownOption(key="Polski", content=ft.Text("Polski")),
            ft.DropdownOption(key="English", content=ft.Text("English")),
        ]
        
    def getthemeoptions():
        return [
            ft.DropdownOption(key="RED", content=ft.Text(_("Red"))),
            ft.DropdownOption(key="ORANGE", content=ft.Text(_("Orange"))),
            ft.DropdownOption(key="YELLOW", content=ft.Text(_("Yellow"))),
            ft.DropdownOption(key="GREEN", content=ft.Text(_("Green"))),
            ft.DropdownOption(key="BLUE", content=ft.Text(_("Blue"))),
            ft.DropdownOption(key="PURPLE", content=ft.Text(_("Purple"))),
            ft.DropdownOption(key="PINK", content=ft.Text(_("Pink"))),
            ft.DropdownOption(key="BROWN", content=ft.Text(_("Brown"))),
            ft.DropdownOption(key="GREY", content=ft.Text(_("Grey"))),
            ft.DropdownOption(key="AMBER", content=ft.Text(_("Amber"))),
            ft.DropdownOption(key="CYAN", content=ft.Text(_("Cyan"))),
            ]

    def onlangchange(e):
        setlanguage(e)
    
    def onthemechange(e):
        setthemecolor(e.data)
    
    
    return ft.Column([
        ft.Text(_("Settings"), size=30, weight="bold"),
        ft.Row([
            ft.Text(_("Language (Requires restart)")),
            ft.Dropdown(
                width=200,
                label=(_("Language")),
                options=getlangoptions(),
                on_change=onlangchange
            ),
        ]),
        
        ft.Row([
            ft.Text(_("Theme (Requires restart)")),
            ft.Dropdown(
                width=200,
                label=(_("Theme")),
                options=getthemeoptions(),
                on_change=onthemechange
            )
        ]),
    ])