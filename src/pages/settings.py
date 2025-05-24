import flet as ft
from constants import *
from utils import setthemecolor, setlanguage, restart, logout
from i18n import _, set_language

def SettingsPage(page):
    # Create the main container to hold everything
    main_container = ft.Container()

    def handle_logout(e):
        logout()
        restart(e.page)
    logout_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text(_("Logout")),
        content=ft.Text(_("Do you want to logout?")),
        actions=[
            ft.TextButton("Yes", on_click=handle_logout),
            ft.TextButton("No", on_click=lambda e: page.close(logout_modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    notification = ft.Banner(
        bgcolor=ft.Colors.AMBER_100,
        leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
        content=ft.Text(
            value=f"{_("Settings changed. Restart required for changes to take effect.")}",
            color=ft.Colors.BLACK,
        ),
        actions=[
            ft.TextButton(
                text=_("Restart"), style=ft.ButtonStyle(color=ft.Colors.BLUE), on_click=lambda e: restart(e.page),
            ),
            ft.TextButton(
                text=_("Later"), style=ft.ButtonStyle(color=ft.Colors.BLUE), on_click=lambda e: hide_notification()
            ),
        ],
    )

    
    def hide_notification():
        page.close(notification)
        main_container.update()
    
    def show_notification():
        page.open(notification)
        main_container.update()
    
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
        show_notification()
    
    def onthemechange(e):
        page.theme = ft.Theme(
        color_scheme_seed=getattr(ft.Colors, e.data),
        font_family="Roboto",
        page_transitions=ft.PageTransitionsTheme(
            macos=ft.PageTransitionTheme.NONE,
            linux=ft.PageTransitionTheme.NONE,
            windows=ft.PageTransitionTheme.NONE
            )
        )
        page.update()
        setthemecolor(e.data)
    
    # Create a column with settings at top and notification container at bottom
    main_content = ft.Column([
        ft.Text(_("Settings"), size=30, weight="bold"),
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(_("Language (Requires restart)")),
                    ft.Dropdown(
                        width=200,
                        label=(_("Language")),
                        options=getlangoptions(),
                        on_change=onlangchange
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text(_("Theme")),
                    ft.Dropdown(
                        width=200,
                        label=(_("Theme")),
                        options=getthemeoptions(),
                        on_change=onthemechange
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ]),
            expand=True  # Make this container expand to push the notification to the bottom
        ),
        ft.Row([
                    ft.Card(
                        content=ft.Container(
                            content=ft.Text(_("Logout")),
                            on_click=lambda e: page.open(logout_modal),
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.RED_400),
                            border_radius=15
                        ),
                        expand=True,
                        height=75
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Text(_("About")),
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLUE_400),
                            border_radius=15,
                            on_click=lambda e: page.go("/about")
                        ),
                        expand=True,
                        height=75
                    ),
                ]),
    ], expand=True)
    
    main_container.content = main_content
    main_container.expand = True  # Make the main container expand
    
    return main_container
