import flet as ft
from constants import *
from utils import setthemecolor, setlanguage, restart
from i18n import _, set_language

def SettingsPage(page):
    # Create the main container to hold everything
    main_container = ft.Container()
    
    # Create a custom notification that we'll show/hide
    notification = ft.Container(
        visible=False,
        bgcolor=ft.colors.AMBER_100,
        border_radius=5,
        padding=10,
        margin=ft.margin.only(bottom=20, left=20, right=20),
        content=ft.Row([
            ft.Icon(ft.icons.INFO_OUTLINED, color=ft.colors.AMBER),
            ft.Text(_("Settings changed. Restart required for changes to take effect."), 
                   color=ft.colors.BLACK, expand=True),
            ft.TextButton(
                text=_("Restart"),
                on_click=lambda e: restart(e.page),
                style=ft.ButtonStyle(color=ft.colors.BLUE),
            ),
            ft.IconButton(
                icon=ft.icons.CLOSE,
                icon_color=ft.colors.GREY_800,
                icon_size=20,
                on_click=lambda e: hide_notification()
            )
        ])
    )

    
    def hide_notification():
        notification.visible = False
        main_container.update()
    
    def show_notification():
        notification.visible = True
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
        # Settings at the top
        ft.Container(
            content=ft.Column([
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
                    ft.Text(_("Theme")),
                    ft.Dropdown(
                        width=200,
                        label=(_("Theme")),
                        options=getthemeoptions(),
                        on_change=onthemechange
                    )
                ]),
            ]),
            expand=True  # Make this container expand to push the notification to the bottom
        ),
        # Notification at the bottom
        notification
    ], expand=True)  # Make the column expand to fill the available space
    
    main_container.content = main_content
    main_container.expand = True  # Make the main container expand
    
    return main_container
